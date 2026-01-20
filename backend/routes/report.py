from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
import os
import sys
from datetime import datetime
from pytz import timezone

IST = timezone('Asia/Kolkata')
report_bp = Blueprint('report', __name__)

# ============================================
# IMPORT RULE-BASED SYSTEM 🔥
# ============================================
try:
    import sys
    import os
    # Add utils directory to path
    utils_path = os.path.join(os.path.dirname(__file__), '..', 'utils')
    if utils_path not in sys.path:
        sys.path.insert(0, utils_path)
    
    from utils.report_parser import MedicalReportParser
    from utils.template_summarizer import TemplateSummarizer
    RULE_BASED_AVAILABLE = True
    print("Rule-based system loaded successfully")
except Exception as e:
    print(f"Rule-based system not available: {e}")
    import traceback
    traceback.print_exc()  # Print full error for debugging
    RULE_BASED_AVAILABLE = False

# Import OCR
try:
    from utils.ocr import process_file
    print("OCR (PyPDF2) loaded successfully")
except Exception as e:
    print(f"OCR not available: {e}")
    process_file = None


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@report_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_report():
    try:
        current_user = get_jwt_identity()

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF, PNG, JPG allowed'}), 400

        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now(IST).strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"

        upload_folder = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)

        print(f"\n{'='*60}")
        print(f"FILE UPLOADED: {filename}")
        print(f"{'='*60}")

        # ============================================
        # STEP 0.5: VERIFICATION (OPTIONAL - only if toggle ON)
        # ============================================

        verify_report_str = request.form.get('verify_report', 'false')
        verify_report = verify_report_str.lower() in ['true', '1', 'yes']

        print(f"Verification Toggle: {'ON' if verify_report else 'OFF'}")

        verification_result = None

        if verify_report:
            try:
                print("VERIFICATION ENABLED - Running forensics...")
                from utils.pdf_forensics import PDFForensics
                
                forensics = PDFForensics()
                verification_result = forensics.analyze_pdf(filepath)
                
                print(f"Verification complete!")
                print(f"   Trust Score: {verification_result['trust_score']}/100")
                print(f"   Risk Level: {verification_result['risk_level']}")
                
            except Exception as e:
                print(f"Verification failed: {e}")
                import traceback
                traceback.print_exc()
                verification_result = {
                    'verified': False,
                    'trust_score': 0,
                    'risk_level': 'Error',
                    'findings': [f'Verification error: {str(e)}'],
                    'recommendations': ['Unable to verify - manual review required']
                }
        else:
            print("Verification: Skipped (toggle OFF)")

        # ============================================
        # STEP 1: EXTRACT TEXT (FAST METHOD FIRST!)
        # ============================================
        extracted_text = None
        extraction_method = None
        
        # Try PyPDF2 first (FASTEST - instant!)
        if callable(process_file):
            try:
                print("Trying PyPDF2 (fast local extraction)...")
                extracted_text = process_file(filepath)
                if extracted_text and len(extracted_text.strip()) > 50:
                    extraction_method = "PyPDF2 (local)"
                    print(f"PyPDF2 SUCCESS! Extracted {len(extracted_text)} chars in <1 second")
            except Exception as e:
                print(f"PyPDF2 failed: {e}")

        # Fallback to AI (only if PyPDF2 failed - for scanned images)
        if not extracted_text:
            try:
                print("PyPDF2 failed, trying Gemini AI (15 sec timeout)...")
                from utils.ai_summarizer import extract_text_from_pdf_with_ai
                extracted_text = extract_text_from_pdf_with_ai(filepath)
                
                if extracted_text:
                    extraction_method = "Gemini AI (fallback)"
                    print(f"Gemini AI SUCCESS! Extracted {len(extracted_text)} chars")
                    
            except Exception as e:
                print(f"Gemini AI failed: {e}")

        # If still no text, fail clearly
        if not extracted_text or len(extracted_text.strip()) < 50:
            return jsonify({
                'error': 'Could not extract text from report',
                'details': 'File may be corrupted, password-protected, or contain only images without OCR'
            }), 400

        print(f"\n{'='*60}")
        print(f"TEXT EXTRACTION COMPLETE")
        print(f"Method: {extraction_method}")
        print(f"Text length: {len(extracted_text)} characters")
        print(f"{'='*60}\n")

        # ============================================
        # STEP 2: RULE-BASED ANALYSIS (YOUR CODE!) 🔥
        # ============================================
        rule_based_summary = None
        parsed_data = None
        
        if RULE_BASED_AVAILABLE and extracted_text:
            try:
                print("RUNNING RULE-BASED SYSTEM (YOUR CODE)...")
                
                # Parse the report
                parser = MedicalReportParser()
                parsed_data = parser.parse_report(
                    extracted_text, 
                    gender="female",  # TODO: Get from user profile
                    age=50  # TODO: Get from user profile
                )
                
                print(f"Parsed {parsed_data['total_tests']} tests from report")
                print(f"Report type: {parsed_data['report_type']}")
                
                # Generate summary using YOUR template system
                summarizer = TemplateSummarizer()
                rule_based_summary = summarizer.generate_summary(parsed_data)
                
                print(f"RULE-BASED SUMMARY GENERATED! ({len(rule_based_summary)} chars)")
                print(f"{'='*60}\n")
                
            except Exception as e:
                print(f"Rule-based system error: {e}")
                import traceback
                traceback.print_exc()

        # ============================================
        # STEP 2.5: MEDICAL VALIDATION (if verification ON)
        # ============================================

        medical_validation = None

        if verify_report and parsed_data:
            try:
                print("MEDICAL VALIDATION - Checking value plausibility...")
                from utils.medical_validator import MedicalValidator
                
                validator = MedicalValidator()
                medical_validation = validator.validate_report(parsed_data)
                
                print(f"Medical validation complete!")
                print(f"   Medical Suspicion: {medical_validation['suspicion_score']}")
                
                # Add medical suspicion to verification score
                if verification_result:
                    # Combine PDF forensics + medical validation
                    combined_suspicion = verification_result.get('suspicion_score', 0) + medical_validation['suspicion_score']
                    
                    # Recalculate trust score
                    verification_result['trust_score'] = max(0, 100 - combined_suspicion)
                    verification_result['findings'].extend(medical_validation['findings'])
                    verification_result['medical_validation'] = medical_validation
                    
                    # Redetermine risk level
                    trust_score = verification_result['trust_score']
                    if trust_score >= 90:
                        verification_result['risk_level'] = "Verified ✅"
                    elif trust_score >= 70:
                        verification_result['risk_level'] = "Low Risk"
                    elif trust_score >= 50:
                        verification_result['risk_level'] = "Medium Risk"
                    elif trust_score >= 30:
                        verification_result['risk_level'] = "High Risk"
                    else:
                        verification_result['risk_level'] = "Critical - Likely Fake"
                    
                    print(f"   Combined Trust Score: {verification_result['trust_score']}/100")
                    print(f"   Final Risk Level: {verification_result['risk_level']}")
                
            except Exception as e:
                print(f"Medical validation failed: {e}")
                import traceback
                traceback.print_exc()

        # ============================================
        # STEP 3: AI ENHANCEMENT (OPTIONAL - only if toggle ON)
        # ============================================

        # Get use_ai flag from request
        use_ai_str = request.form.get('use_ai', 'false')
        use_ai = use_ai_str.lower() in ['true', '1', 'yes']

        print(f"AI Enhancement Toggle: {'ON' if use_ai else 'OFF'}")

        ai_enhanced_summary = None
        ai_enhancement_success = False  # Track if AI actually worked

        if use_ai and rule_based_summary:
            try:
                print("AI ENHANCEMENT ENABLED - Polishing summary...")
                from utils.ai_summarizer import enhance_summary_with_ai
                
                ai_enhanced_summary = enhance_summary_with_ai(rule_based_summary)
                
                # Check if AI actually returned something different
                if ai_enhanced_summary and ai_enhanced_summary != rule_based_summary:
                    ai_enhancement_success = True
                    print(f"AI enhancement SUCCESS!")
                else:
                    print(f"AI enhancement returned same content (likely failed)")
                    ai_enhanced_summary = None
                
            except Exception as e:
                print(f"AI enhancement failed: {e}")
                import traceback
                traceback.print_exc()
                ai_enhanced_summary = None

        # Use enhanced version if available AND successful, otherwise rule-based
        final_summary = ai_enhanced_summary if ai_enhancement_success else rule_based_summary

        print(f"\n{'='*60}")
        print(f"FINAL SUMMARY METHOD:")
        print(f"   Using: {'AI Enhanced' if ai_enhancement_success else 'Rule-based Only'}")
        print(f"   Length: {len(final_summary)} characters")
        print(f"{'='*60}\n")

        # ============================================
        # STEP 4: AI FALLBACK (ONLY IF RULE-BASED FAILED)
        # ============================================
        ai_summary = None
        quick_summary = None
        
        if not rule_based_summary:
            print("Rule-based failed, using AI fallback...")
            try:
                from utils.ai_summarizer import generate_medical_summary, generate_quick_summary
                ai_summary = generate_medical_summary(extracted_text)
                quick_summary = generate_quick_summary(extracted_text)
                print("AI summary generated (fallback)")
            except Exception as e:
                print(f"AI summary also failed: {e}")
                return jsonify({'error': 'Summary generation failed completely'}), 500
        else:
            print("Using rule-based summary")
            # Create a simple quick summary from rule-based
            quick_summary = f"Analysis of {parsed_data['report_type']} - {parsed_data['total_tests']} tests analyzed"

        # ============================================
        # STEP 5: PREPARE FINAL SUMMARY
        # ============================================
        
        # final_summary already set above (either ai_enhanced_summary or rule_based_summary)
        if not final_summary:
            return jsonify({'error': 'Summary generation failed'}), 500

        summary_data = {
            'plain_language_summary': final_summary,
            'quick_summary': quick_summary,
            'status': 'success',
            'word_count': len(extracted_text.split()),
            'method': 'rule_based_with_ai' if ai_enhancement_success else 'rule_based_only',
            'extraction_method': extraction_method,
            'tests_found': parsed_data['total_tests'] if parsed_data else 0,
            'report_type': parsed_data['report_type'] if parsed_data else 'Unknown',
            'ai_enhanced': ai_enhancement_success,
            'verification': verification_result,
            'verification_enabled': verify_report,
            'medical_validation': medical_validation
        }

        print(f"\n{'='*60}")
        print(f"FINAL SUMMARY PREPARED")
        print(f"Method: {summary_data['method']}")
        print(f"Extraction: {extraction_method}")
        print(f"Tests found: {summary_data['tests_found']}")
        print(f"{'='*60}\n")

        # ============================================
        # STEP 6: SAVE TO DATABASE
        # ============================================
        reports_collection = db['reports']

        report_data = {
            'user_email': current_user,
            'filename': unique_filename,
            'original_filename': filename,
            'filepath': filepath,
            'extracted_text': extracted_text,
            'extraction_method': extraction_method,
            'summary': summary_data,
            'plain_language_summary': final_summary,
            'rule_based_summary': rule_based_summary,
            'ai_enhanced_summary': ai_enhanced_summary,
            'ai_summary': ai_summary,
            'use_ai': use_ai,
            'verification': verification_result,
            'verification_enabled': verify_report,
            'medical_validation': medical_validation,
            'parsed_data': parsed_data,
            'uploaded_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p"),
            'processed': True
        }

        result = reports_collection.insert_one(report_data)
        report_id = str(result.inserted_id)
        
        print(f"Saved to database - Report ID: {report_id}\n")

        # Update user's reports array
        users_collection = db['users']
        users_collection.update_one(
            {'email': current_user},
            {'$push': {'reports': report_id}}
        )

        return jsonify({
            'message': 'Report processed successfully',
            'report_id': report_id,
            'filename': filename,
            'summary': summary_data,
            'plain_language_summary': final_summary,
            'method_used': summary_data['method'],
            'extraction_method': extraction_method,
            'tests_analyzed': summary_data['tests_found'],
            'ai_enhanced': summary_data['ai_enhanced'],
            'verification_enabled': summary_data['verification_enabled']
        }), 200

    except Exception as e:
        print(f"\nERROR in upload_report:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e)}), 500


@report_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        current_user = get_jwt_identity()

        reports_collection = db['reports']
        reports = list(reports_collection.find(
            {'user_email': current_user}
        ).sort('uploaded_at', -1))

        formatted_reports = []
        for report in reports:
            formatted_reports.append({
                'id': str(report['_id']),
                'filename': report.get('original_filename', 'Unknown'),
                'uploaded_at': report.get('uploaded_at'),
                'plain_summary': report.get('plain_language_summary', 'No summary available'),
                'method': report.get('summary', {}).get('method', 'unknown'),
                'extraction_method': report.get('extraction_method', 'unknown'),
                'report_type': report.get('summary', {}).get('report_type', 'Unknown'),
                'ai_enhanced': report.get('summary', {}).get('ai_enhanced', False),
                'use_ai': report.get('use_ai', False),
                'verification_enabled': report.get('verification_enabled', False)
            })

        return jsonify({
            'message': 'History retrieved successfully',
            'total_reports': len(formatted_reports),
            'reports': formatted_reports
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@report_bp.route('/details/<report_id>', methods=['GET'])
@jwt_required()
def get_report_details(report_id):
    try:
        from bson.objectid import ObjectId
        current_user = get_jwt_identity()

        reports_collection = db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })

        if not report:
            return jsonify({'error': 'Report not found'}), 404

        return jsonify({
            'id': str(report['_id']),
            'filename': report.get('original_filename'),
            'uploaded_at': report.get('uploaded_at'),
            'extracted_text': report.get('extracted_text'),
            'summary': report.get('summary'),
            'plain_language_summary': report.get('plain_language_summary'),
            'method_used': report.get('summary', {}).get('method', 'unknown'),
            'extraction_method': report.get('extraction_method', 'unknown'),
            'parsed_data': report.get('parsed_data'),
            'ai_enhanced': report.get('summary', {}).get('ai_enhanced', False),
            'use_ai': report.get('use_ai', False),
            'rule_based_summary': report.get('rule_based_summary'),
            'ai_enhanced_summary': report.get('ai_enhanced_summary'),
            'verification': report.get('verification'),
            'verification_enabled': report.get('verification_enabled', False),
            'medical_validation': report.get('medical_validation')
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500