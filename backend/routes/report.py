from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
import os
import sys
import re
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
        
        # Try PyPDF2 first (FASTEST - instant!) - ONLY for PDFs
        if filepath.lower().endswith('.pdf') and callable(process_file):
            try:
                print("Trying PyPDF2 (fast local extraction)...")
                extracted_text = process_file(filepath)
                
                # ✅ FIX: Check if text is meaningful (more than 50 chars)
                if extracted_text and len(extracted_text.strip()) > 50:
                    extraction_method = "PyPDF2 (local)"
                    print(f"✅ PyPDF2 SUCCESS! Extracted {len(extracted_text)} chars in <1 second")
                else:
                    # PyPDF2 returned empty/minimal text - likely scanned
                    print(f"⚠️ PyPDF2 returned minimal text ({len(extracted_text or '')} chars) - likely scanned PDF")
                    extracted_text = None  # Reset to trigger AI fallback
            except Exception as e:
                print(f"❌ PyPDF2 failed: {e}")
                extracted_text = None

        # ✅ FIX: Fallback to Gemini AI OCR (for scanned PDFs or when PyPDF2 fails)
        if not extracted_text:
            try:
                print("📸 PyPDF2 failed/insufficient text → Trying Gemini AI OCR...")
                from utils.ai_summarizer import extract_text_from_pdf_with_ai
                
                # This works for both scanned PDFs and images
                extracted_text = extract_text_from_pdf_with_ai(filepath)
                
                if extracted_text and len(extracted_text.strip()) > 50:
                    extraction_method = "Gemini AI OCR"
                    print(f"✅ Gemini AI SUCCESS! Extracted {len(extracted_text)} chars")
                else:
                    print(f"❌ Gemini AI returned insufficient text")
                    extracted_text = None
                    
            except Exception as e:
                print(f"❌ Gemini AI OCR failed: {e}")
                import traceback
                traceback.print_exc()

        # ✅ FIX: Final validation - if still no text, return clear error
        if not extracted_text or len(extracted_text.strip()) < 50:
            error_msg = 'Could not extract text from report'
            details = 'File may be corrupted, password-protected, or severely damaged. '
            
            if filepath.lower().endswith('.pdf'):
                details += 'PDF appears to be scanned but OCR failed. Try a clearer scan or digital PDF.'
            else:
                details += 'Image quality may be too low for text recognition.'
            
            return jsonify({
                'error': error_msg,
                'details': details
            }), 400

        print(f"\n{'='*60}")
        print(f"✅ TEXT EXTRACTION COMPLETE")
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


# ============================================
# 🔥 NEW FEATURE: COMPARE TWO REPORTS 🔥
# ============================================

@report_bp.route('/compare', methods=['POST'])
@jwt_required()
def compare_reports():
    """
    Compare two uploaded medical reports
    Returns matching tests with their values and changes
    """
    try:
        current_user = get_jwt_identity()
        
        # Get uploaded files
        if 'report1' not in request.files or 'report2' not in request.files:
            return jsonify({'error': 'Both reports are required'}), 400
        
        file1 = request.files['report1']
        file2 = request.files['report2']
        
        if not file1.filename or not file2.filename:
            return jsonify({'error': 'Both files must have filenames'}), 400
        
        # Validate file types
        if not (file1.filename.endswith('.pdf') and file2.filename.endswith('.pdf')):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save files temporarily
        upload_folder = os.path.join(os.getcwd(), 'uploads', 'temp')
        os.makedirs(upload_folder, exist_ok=True)
        
        filename1 = secure_filename(f"temp1_{current_user}_{file1.filename}")
        filename2 = secure_filename(f"temp2_{current_user}_{file2.filename}")
        
        filepath1 = os.path.join(upload_folder, filename1)
        filepath2 = os.path.join(upload_folder, filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        print(f"\n{'='*60}")
        print(f"COMPARING REPORTS:")
        print(f"Report 1: {file1.filename}")
        print(f"Report 2: {file2.filename}")
        print(f"{'='*60}\n")
        
        # Extract text from both PDFs
        text1 = None
        text2 = None
        
        # Try PyPDF2 first for both
        if callable(process_file):
            try:
                text1 = process_file(filepath1)
                if not text1 or len(text1.strip()) < 50:
                    text1 = None
            except:
                text1 = None
            
            try:
                text2 = process_file(filepath2)
                if not text2 or len(text2.strip()) < 50:
                    text2 = None
            except:
                text2 = None
        
        # Fallback to AI OCR if needed
        if not text1:
            try:
                from utils.ai_summarizer import extract_text_from_pdf_with_ai
                text1 = extract_text_from_pdf_with_ai(filepath1)
            except Exception as e:
                print(f"Failed to extract text from report 1: {e}")
        
        if not text2:
            try:
                from utils.ai_summarizer import extract_text_from_pdf_with_ai
                text2 = extract_text_from_pdf_with_ai(filepath2)
            except Exception as e:
                print(f"Failed to extract text from report 2: {e}")
        
        if not text1 or not text2:
            return jsonify({'error': 'Failed to extract text from one or both reports'}), 400
        
        print(f"✅ Text extracted from both reports")
        print(f"Report 1: {len(text1)} chars")
        print(f"Report 2: {len(text2)} chars\n")
        
        # Extract test results from both
        tests1 = extract_test_results(text1)
        tests2 = extract_test_results(text2)
        
        print(f"Found {len(tests1)} tests in Report 1")
        print(f"Found {len(tests2)} tests in Report 2\n")
        
        # Find matching tests
        comparisons = []
        test_names1 = {test['name']: test for test in tests1}
        test_names2 = {test['name']: test for test in tests2}
        
        for test_name in test_names1:
            if test_name in test_names2:
                test1 = test_names1[test_name]
                test2 = test_names2[test_name]
                
                # Only compare if units match
                if test1['unit'] == test2['unit']:
                    comparisons.append({
                        'name': test_name,
                        'value1': test1['value'],
                        'value2': test2['value'],
                        'unit': test1['unit']
                    })
        
        print(f"✅ Found {len(comparisons)} matching tests\n")
        
        # Calculate summary statistics
        improved = 0
        worsened = 0
        stable = 0
        
        # Tests where lower is better
        lower_is_better = ['cholesterol', 'ldl', 'triglycerides', 'glucose', 'hba1c', 'creatinine', 'urea', 'bilirubin']
        
        for comp in comparisons:
            change = comp['value2'] - comp['value1']
            is_lower_better = any(term in comp['name'].lower() for term in lower_is_better)
            
            if abs(change) < 0.01:  # Essentially no change
                stable += 1
            elif (change < 0 and is_lower_better) or (change > 0 and not is_lower_better):
                improved += 1
            else:
                worsened += 1
        
        # Extract dates from reports
        date1 = extract_date_from_text(text1)
        date2 = extract_date_from_text(text2)
        
        print(f"Summary:")
        print(f"  Improved: {improved}")
        print(f"  Worsened: {worsened}")
        print(f"  Stable: {stable}")
        print(f"{'='*60}\n")
        
        # Clean up temporary files
        try:
            os.remove(filepath1)
            os.remove(filepath2)
        except:
            pass
        
        return jsonify({
            'success': True,
            'comparisons': comparisons,
            'summary': {
                'total_tests': len(comparisons),
                'improved_count': improved,
                'worsened_count': worsened,
                'stable_count': stable
            },
            'report1_date': date1,
            'report2_date': date2
        }), 200
        
    except Exception as e:
        print(f"\nERROR in compare_reports:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': f'Failed to compare reports: {str(e)}'}), 500


def extract_test_results(text):
    """
    Extract test results from medical report text
    Returns list of {name, value, unit}
    """
    tests = []
    seen_names = set()
    
    # Valid medical units (lowercase for comparison)
    valid_units = [
        'mg/dl', 'g/dl', 'mmol/l', 'meq/l', 'iu/l', 'u/l',
        '%', 'percent', 'ratio',
        'ng/ml', 'pg/ml', 'miu/ml', 'uiu/ml', 'pmol/l',
        'cells/cumm', 'thou/cumm', 'mill/cumm',
        'sec', 'seconds', 'mm/hr', 'fl', 'mcg/dl', 'umol/l',
        'g/l', 'mg/l', 'ug/l', 'nmol/l'
    ]
    
    # Strict blacklist - only obvious non-medical terms
    blacklist = [
        'floor no', 'street name', 'apartment', 'building name',
        'pincode', 'zip code', 
        'barcode', 'labcode', 'page',
        'sample collected', 'sample received', 'report released',
        'patient name', 'ref. by', 'test asked',
        'technologies ltd', 'pvt ltd',
        '560025', 'richmond', 'bangalore', 'serpentine'
    ]
    
    # Pattern: TEST_NAME value unit
    # Looking for lines with this structure
    lines = text.split('\n')
    
    for line in lines:
        # Skip very short lines
        if len(line) < 15:
            continue
        
        # Try to find: word(s) followed by number followed by unit
        # Use multiple patterns
        patterns = [
            # Pattern 1: TEST NAME TECH value unit
            r'([A-Z][A-Za-z0-9\s\-/()]+?)\s+[A-Z\.]+\s+([\d.]+)\s+([a-zA-Z/%]+)',
            # Pattern 2: TEST NAME value unit  
            r'^([A-Z][A-Za-z0-9\s\-/()]+?)\s+([\d.]+)\s+([a-zA-Z/%]+)\s*$',
            # Pattern 3: TEST NAME: value unit
            r'([A-Z][A-Za-z0-9\s\-/()]+?):\s+([\d.]+)\s+([a-zA-Z/%]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                test_name = match.group(1).strip()
                value_str = match.group(2).strip()
                unit = match.group(3).strip()
                
                # Basic validation
                if len(test_name) < 3 or len(test_name) > 60:
                    continue
                
                # Check if unit is valid
                unit_lower = unit.lower()
                if not any(valid_unit in unit_lower or unit_lower in valid_unit for valid_unit in valid_units):
                    continue
                
                # Check blacklist (only exact phrases)
                test_lower = test_name.lower()
                if any(black in test_lower for black in blacklist):
                    continue
                
                # Skip if test name is all numbers
                if test_name.replace(' ', '').replace('-', '').isdigit():
                    continue
                
                # Skip duplicates
                if test_name in seen_names:
                    continue
                
                try:
                    value = float(value_str)
                    
                    # Skip unrealistic values
                    if value < 0 or value > 500000:
                        continue
                    
                    tests.append({
                        'name': test_name,
                        'value': value,
                        'unit': unit
                    })
                    seen_names.add(test_name)
                    
                except ValueError:
                    continue
                
                break  # Found match, move to next line
    
    return tests


def extract_date_from_text(text):
    """
    Try to extract a date from the report text
    Returns ISO format date string or None
    """
    # Common date patterns
    date_patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # DD/MM/YYYY or DD-MM-YYYY
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD or YYYY-MM-DD
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})',  # Month DD, YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                groups = match.groups()
                if len(groups) == 3:
                    if pattern.startswith(r'(\d{1,2})'):
                        # DD/MM/YYYY format
                        day, month, year = groups
                        date_obj = datetime(int(year), int(month), int(day))
                    elif pattern.startswith(r'(\d{4})'):
                        # YYYY/MM/DD format
                        year, month, day = groups
                        date_obj = datetime(int(year), int(month), int(day))
                    else:
                        # Month name format
                        month_name, day, year = groups
                        month_num = datetime.strptime(month_name[:3], '%b').month
                        date_obj = datetime(int(year), month_num, int(day))
                    
                    return date_obj.isoformat()
            except:
                continue
    
    return None


# ============================================
# 🔥 HEALTH RISK CALCULATOR ENDPOINT 🔥
# ============================================

@report_bp.route('/calculate-risks/<report_id>', methods=['GET'])
@jwt_required()
def calculate_health_risks(report_id):
    """
    Calculate health risks based on a report's test values
    Returns cardiovascular risk, diabetes risk, and overall health score
    """
    try:
        from bson.objectid import ObjectId
        current_user = get_jwt_identity()
        
        # Fetch the report
        reports_collection = db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Get parsed data from report
        parsed_data = report.get('parsed_data', {})
        
        if not parsed_data or 'tests' not in parsed_data:
            return jsonify({'error': 'No test data available for risk calculation'}), 400
        
        # Extract test values
        tests = parsed_data['tests']
        test_values = {}
        
        for test in tests:
            test_name = test.get('name', '').lower()
            test_value = test.get('value')
            
            # Map test names to standardized keys
            if 'cholesterol' in test_name and 'total' in test_name:
                test_values['total_cholesterol'] = test_value
            elif 'hdl' in test_name:
                test_values['hdl'] = test_value
            elif 'ldl' in test_name:
                test_values['ldl'] = test_value
            elif 'triglyceride' in test_name:
                test_values['triglycerides'] = test_value
            elif 'hba1c' in test_name or 'a1c' in test_name:
                test_values['hba1c'] = test_value
            elif 'glucose' in test_name and 'fasting' in test_name:
                test_values['fasting_glucose'] = test_value
            elif 'creatinine' in test_name:
                test_values['creatinine'] = test_value
            elif 'urea' in test_name or 'bun' in test_name:
                test_values['urea'] = test_value
        
        print(f"Extracted test values: {test_values}")
        
        # Calculate risks
        risks = calculate_all_risks(test_values)
        
        return jsonify({
            'success': True,
            'risks': risks,
            'report_id': report_id,
            'calculated_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p")
        }), 200
        
    except Exception as e:
        print(f"\nERROR in calculate_health_risks:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e)}), 500


def calculate_all_risks(test_values):
    """
    Calculate all health risks based on test values
    Returns a dictionary with risk assessments
    """
    risks = {
        'overall_score': 100,
        'cardiovascular': None,
        'diabetes': None,
        'kidney': None,
        'recommendations': []
    }
    
    # ============================================
    # CARDIOVASCULAR RISK ASSESSMENT
    # ============================================
    cardio_risk = assess_cardiovascular_risk(test_values)
    risks['cardiovascular'] = cardio_risk
    
    # Deduct from overall score based on cardio risk
    if cardio_risk['level'] == 'HIGH':
        risks['overall_score'] -= 15
        risks['recommendations'].extend(cardio_risk['recommendations'])
    elif cardio_risk['level'] == 'MEDIUM':
        risks['overall_score'] -= 8
        risks['recommendations'].extend(cardio_risk['recommendations'])
    
    # ============================================
    # DIABETES RISK ASSESSMENT
    # ============================================
    diabetes_risk = assess_diabetes_risk(test_values)
    risks['diabetes'] = diabetes_risk
    
    # Deduct from overall score based on diabetes risk
    if diabetes_risk['level'] == 'DIABETIC':
        risks['overall_score'] -= 15
        risks['recommendations'].extend(diabetes_risk['recommendations'])
    elif diabetes_risk['level'] == 'PREDIABETIC':
        risks['overall_score'] -= 10
        risks['recommendations'].extend(diabetes_risk['recommendations'])
    
    # ============================================
    # KIDNEY HEALTH ASSESSMENT
    # ============================================
    kidney_health = assess_kidney_health(test_values)
    risks['kidney'] = kidney_health
    
    # Deduct from overall score based on kidney health
    if kidney_health['level'] == 'HIGH_RISK':
        risks['overall_score'] -= 15
        risks['recommendations'].extend(kidney_health['recommendations'])
    elif kidney_health['level'] == 'MODERATE_RISK':
        risks['overall_score'] -= 8
        risks['recommendations'].extend(kidney_health['recommendations'])
    
    # Ensure score doesn't go below 0
    risks['overall_score'] = max(0, risks['overall_score'])
    
    # Determine overall health status
    if risks['overall_score'] >= 90:
        risks['overall_status'] = 'Excellent'
        risks['overall_message'] = 'Your health markers are excellent! Keep up the good work.'
    elif risks['overall_score'] >= 75:
        risks['overall_status'] = 'Good'
        risks['overall_message'] = 'Your health is good overall. Follow the recommendations to maintain it.'
    elif risks['overall_score'] >= 60:
        risks['overall_status'] = 'Fair'
        risks['overall_message'] = 'Some health markers need attention. Please follow the recommendations.'
    elif risks['overall_score'] >= 40:
        risks['overall_status'] = 'Poor'
        risks['overall_message'] = 'Multiple health concerns detected. Consult your doctor soon.'
    else:
        risks['overall_status'] = 'Critical'
        risks['overall_message'] = 'Immediate medical attention recommended. Please consult your doctor.'
    
    # Remove duplicate recommendations
    risks['recommendations'] = list(set(risks['recommendations']))
    
    return risks


def assess_cardiovascular_risk(test_values):
    """
    Assess cardiovascular disease risk based on lipid profile
    """
    risk = {
        'level': 'UNKNOWN',
        'score': 0,
        'factors': [],
        'recommendations': []
    }
    
    total_chol = test_values.get('total_cholesterol')
    hdl = test_values.get('hdl')
    ldl = test_values.get('ldl')
    triglycerides = test_values.get('triglycerides')
    
    risk_points = 0
    
    # Total Cholesterol assessment
    if total_chol is not None:
        if total_chol >= 240:
            risk_points += 3
            risk['factors'].append(f'High Total Cholesterol: {total_chol} mg/dL (>= 240)')
        elif total_chol >= 200:
            risk_points += 2
            risk['factors'].append(f'Borderline High Cholesterol: {total_chol} mg/dL (200-239)')
        else:
            risk['factors'].append(f'Normal Total Cholesterol: {total_chol} mg/dL (<200)')
    
    # HDL assessment
    if hdl is not None:
        if hdl < 40:
            risk_points += 2
            risk['factors'].append(f'Low HDL (Good Cholesterol): {hdl} mg/dL (<40)')
        elif hdl >= 60:
            risk_points -= 1  # Protective factor
            risk['factors'].append(f'High HDL (Good Cholesterol): {hdl} mg/dL (>=60) - Protective!')
        else:
            risk['factors'].append(f'Normal HDL: {hdl} mg/dL (40-60)')
    
    # LDL assessment
    if ldl is not None:
        if ldl >= 160:
            risk_points += 3
            risk['factors'].append(f'High LDL (Bad Cholesterol): {ldl} mg/dL (>=160)')
        elif ldl >= 130:
            risk_points += 2
            risk['factors'].append(f'Borderline High LDL: {ldl} mg/dL (130-159)')
        elif ldl >= 100:
            risk_points += 1
            risk['factors'].append(f'Near Optimal LDL: {ldl} mg/dL (100-129)')
        else:
            risk['factors'].append(f'Optimal LDL: {ldl} mg/dL (<100)')
    
    # Triglycerides assessment
    if triglycerides is not None:
        if triglycerides >= 200:
            risk_points += 2
            risk['factors'].append(f'High Triglycerides: {triglycerides} mg/dL (>=200)')
        elif triglycerides >= 150:
            risk_points += 1
            risk['factors'].append(f'Borderline High Triglycerides: {triglycerides} mg/dL (150-199)')
        else:
            risk['factors'].append(f'Normal Triglycerides: {triglycerides} mg/dL (<150)')
    
    # Determine risk level
    if risk_points >= 5:
        risk['level'] = 'HIGH'
        risk['recommendations'] = [
            'Consult a cardiologist immediately',
            'Consider starting cholesterol-lowering medication',
            'Follow a heart-healthy diet (low saturated fat)',
            'Exercise at least 30 minutes daily',
            'Stop smoking if applicable'
        ]
    elif risk_points >= 3:
        risk['level'] = 'MEDIUM'
        risk['recommendations'] = [
            'Monitor cholesterol levels regularly',
            'Reduce saturated fat and trans fat intake',
            'Increase physical activity to 30 mins daily',
            'Maintain healthy weight',
            'Consider consulting a dietitian'
        ]
    else:
        risk['level'] = 'LOW'
        risk['recommendations'] = [
            'Maintain current healthy lifestyle',
            'Continue regular exercise',
            'Annual cholesterol screening recommended'
        ]
    
    risk['score'] = risk_points
    
    return risk


def assess_diabetes_risk(test_values):
    """
    Assess diabetes risk based on glucose and HbA1c levels
    """
    risk = {
        'level': 'UNKNOWN',
        'factors': [],
        'recommendations': []
    }
    
    hba1c = test_values.get('hba1c')
    fasting_glucose = test_values.get('fasting_glucose')
    
    # HbA1c assessment (primary indicator)
    if hba1c is not None:
        if hba1c >= 6.5:
            risk['level'] = 'DIABETIC'
            risk['factors'].append(f'HbA1c: {hba1c}% (>=6.5% indicates diabetes)')
            risk['recommendations'] = [
                'Consult an endocrinologist immediately',
                'Start diabetes management plan',
                'Monitor blood sugar regularly',
                'Follow diabetic diet plan',
                'Exercise 30-45 minutes daily',
                'Check for complications (eyes, kidneys, feet)'
            ]
        elif hba1c >= 5.7:
            risk['level'] = 'PREDIABETIC'
            risk['factors'].append(f'HbA1c: {hba1c}% (5.7-6.4% indicates prediabetes)')
            risk['recommendations'] = [
                'Lifestyle changes to prevent diabetes',
                'Reduce sugar and refined carbohydrate intake',
                'Lose 5-10% body weight if overweight',
                'Exercise 150 minutes per week',
                'Monitor HbA1c every 3-6 months',
                'Consider consulting a dietitian'
            ]
        else:
            risk['level'] = 'NORMAL'
            risk['factors'].append(f'HbA1c: {hba1c}% (<5.7% is normal)')
            risk['recommendations'] = [
                'Maintain healthy lifestyle',
                'Annual HbA1c screening recommended',
                'Balanced diet with limited processed sugars'
            ]
    
    # Fasting Glucose assessment (secondary indicator)
    if fasting_glucose is not None:
        if fasting_glucose >= 126:
            if risk['level'] != 'DIABETIC':
                risk['level'] = 'DIABETIC'
            risk['factors'].append(f'Fasting Glucose: {fasting_glucose} mg/dL (>=126 indicates diabetes)')
        elif fasting_glucose >= 100:
            if risk['level'] == 'UNKNOWN' or risk['level'] == 'NORMAL':
                risk['level'] = 'PREDIABETIC'
            risk['factors'].append(f'Fasting Glucose: {fasting_glucose} mg/dL (100-125 indicates prediabetes)')
        else:
            if risk['level'] == 'UNKNOWN':
                risk['level'] = 'NORMAL'
            risk['factors'].append(f'Fasting Glucose: {fasting_glucose} mg/dL (<100 is normal)')
    
    return risk


def assess_kidney_health(test_values):
    """
    Assess kidney health based on creatinine and urea levels
    """
    risk = {
        'level': 'UNKNOWN',
        'factors': [],
        'recommendations': []
    }
    
    creatinine = test_values.get('creatinine')
    urea = test_values.get('urea')
    
    risk_points = 0
    
    # Creatinine assessment
    if creatinine is not None:
        if creatinine > 1.3:  # Elevated for most adults
            risk_points += 2
            risk['factors'].append(f'Elevated Creatinine: {creatinine} mg/dL (>1.3)')
        elif creatinine > 1.1:
            risk_points += 1
            risk['factors'].append(f'Borderline Creatinine: {creatinine} mg/dL (>1.1)')
        else:
            risk['factors'].append(f'Normal Creatinine: {creatinine} mg/dL (<=1.1)')
    
    # Urea assessment
    if urea is not None:
        if urea > 45:  # Elevated
            risk_points += 2
            risk['factors'].append(f'Elevated Urea: {urea} mg/dL (>45)')
        elif urea > 40:
            risk_points += 1
            risk['factors'].append(f'Borderline Urea: {urea} mg/dL (>40)')
        else:
            risk['factors'].append(f'Normal Urea: {urea} mg/dL (<=40)')
    
    # Determine risk level
    if risk_points >= 3:
        risk['level'] = 'HIGH_RISK'
        risk['recommendations'] = [
            'Consult a nephrologist immediately',
            'Get kidney function tests (eGFR)',
            'Stay well hydrated',
            'Limit protein intake',
            'Monitor blood pressure regularly',
            'Avoid nephrotoxic medications'
        ]
    elif risk_points >= 1:
        risk['level'] = 'MODERATE_RISK'
        risk['recommendations'] = [
            'Monitor kidney function regularly',
            'Stay hydrated (8-10 glasses water daily)',
            'Limit sodium intake',
            'Control blood pressure and blood sugar',
            'Recheck kidney tests in 3 months'
        ]
    else:
        risk['level'] = 'NORMAL'
        risk['recommendations'] = [
            'Kidney function is normal',
            'Maintain adequate hydration',
            'Annual kidney screening recommended'
        ]
    
    return risk