from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import sys
import re
import time
from datetime import datetime
from pytz import timezone
from difflib import SequenceMatcher
IST = timezone('Asia/Kolkata')
report_bp = Blueprint('report', __name__)
# ============================================
# IMPORT VALIDATION & DEPENDENCY CHECK
# ============================================
try:
    from bson import ObjectId
    BSON_AVAILABLE = True
except ImportError:
    BSON_AVAILABLE = False
    print("⚠️ BSON not available - MongoDB features will be limited")
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
    print("✅ Rule-based system loaded successfully")
except Exception as e:
    print(f"❌ Rule-based system not available: {e}")
    import traceback
    traceback.print_exc() # Print full error for debugging
    RULE_BASED_AVAILABLE = False
# Import OCR
try:
    from utils.ocr import process_file
    print("✅ OCR (PyPDF2) loaded successfully")
    OCR_AVAILABLE = True
except Exception as e:
    print(f"❌ OCR not available: {e}")
    process_file = None
    OCR_AVAILABLE = False
# ============================================
# CONSTANTS
# ============================================
MAX_FILE_SIZE = 50 * 1024 * 1024 # 50MB
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'jfif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def validate_file_size(file):
    """Validate file size before processing"""
    file.seek(0, 2) # Seek to end
    size = file.tell()
    file.seek(0) # Reset to beginning
    return size <= MAX_FILE_SIZE, size
# ============================================
# REGEX EXTRACTION FUNCTION (ADDED FOR FIX)
# ============================================
def extract_tests_from_raw_text(text):
    """
    🔥 FINAL FIX - Handles PyPDF2's column-based extraction
    
    PyPDF2 extracts in column format where values are on separate lines
    """
    tests = []
    
    print(f"\n{'='*60}")
    print(f"📄 REGEX EXTRACTION (MULTILINE COLUMN MODE)")
    print(f"{'='*60}\n")
    
    # Normalize whitespace but keep structure
    text_clean = re.sub(r' +', ' ', text)
    
    # ────────────────────────────────────────────
    # TOTAL CHOLESTEROL
    # ────────────────────────────────────────────
    match = re.search(r'TOTAL\s+CHOLESTEROL.*?PHOTOMETRY.*?(\d+)\s*(?:mg/dL|H\.P\.L\.C)', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(0)
        value_match = re.search(r'PHOTOMETRY\s+(\d+)', section)
        if value_match:
            value = float(value_match.group(1))
            tests.append({'name': 'Total Cholesterol', 'value': value, 'unit': 'mg/dL', 'status': 'NORMAL'})
            print(f"   ✓ Total Cholesterol = {value} mg/dL")
    
    # ────────────────────────────────────────────
    # HDL CHOLESTEROL
    # ────────────────────────────────────────────
    match = re.search(r'HDL\s+CHOLESTEROL.*?(?:DIRECT|PHOTOMETRY).*?(\d+)\s*(?:mg/dL|H\.P\.L\.C)', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(0)
        value_match = re.search(r'(?:DIRECT|PHOTOMETRY)\s+(\d+)', section)
        if value_match:
            value = float(value_match.group(1))
            tests.append({'name': 'HDL', 'value': value, 'unit': 'mg/dL', 'status': 'NORMAL'})
            print(f"   ✓ HDL = {value} mg/dL")
    
    # ────────────────────────────────────────────
    # LDL CHOLESTEROL
    # ────────────────────────────────────────────
    match = re.search(r'LDL\s+CHOLESTEROL.*?(?:DIRECT|PHOTOMETRY).*?(\d+)\s*(?:mg/dL|H\.P\.L\.C)', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(0)
        value_match = re.search(r'(?:DIRECT|PHOTOMETRY)\s+(\d+)', section)
        if value_match:
            value = float(value_match.group(1))
            tests.append({'name': 'LDL', 'value': value, 'unit': 'mg/dL', 'status': 'NORMAL'})
            print(f"   ✓ LDL = {value} mg/dL")
    
    # ────────────────────────────────────────────
    # TRIGLYCERIDES
    # ────────────────────────────────────────────
    match = re.search(r'TRIGLYCERIDES\s+PHOTOMETRY.*?(\d+)\s*(?:mg/dL|H\.P\.L\.C)', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(0)
        value_match = re.search(r'PHOTOMETRY\s+(\d+)', section)
        if value_match:
            value = float(value_match.group(1))
            tests.append({'name': 'Triglycerides', 'value': value, 'unit': 'mg/dL', 'status': 'NORMAL'})
            print(f"   ✓ Triglycerides = {value} mg/dL")
    
    # ────────────────────────────────────────────
    # VLDL CHOLESTEROL
    # ────────────────────────────────────────────
    match = re.search(r'VLDL\s+CHOLESTEROL.*?CALCULATED.*?([\d.]+)\s*(?:mg/dL|5\s*-)', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(0)
        value_match = re.search(r'CALCULATED\s+([\d.]+)', section)
        if value_match:
            value = float(value_match.group(1))
            if 5 <= value <= 100:  # Sanity check
                tests.append({'name': 'VLDL', 'value': value, 'unit': 'mg/dL', 'status': 'NORMAL'})
                print(f"   ✓ VLDL = {value} mg/dL")
    
    # ────────────────────────────────────────────
    # HbA1c
    # ────────────────────────────────────────────
    match = re.search(r'([\d.]+)\s+H\.P\.L\.C\s+%', text_clean, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        if 3.0 <= value <= 15.0:  # Sanity check
            tests.append({'name': 'HbA1c', 'value': value, 'unit': '%', 'status': 'NORMAL'})
            print(f"   ✓ HbA1c = {value} %")
    
    # ────────────────────────────────────────────
    # TROPONIN I
    # ────────────────────────────────────────────
    match = re.search(r'TROPONIN\s+I.*?C\.M\.I\.A\s+([\d.]+)\s*pg/mL', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        value = float(match.group(1))
        if 0.1 <= value <= 1000:  # Sanity check
            tests.append({'name': 'Troponin I', 'value': value, 'unit': 'pg/mL', 'status': 'NORMAL'})
            print(f"   ✓ Troponin I = {value} pg/mL")
    
    # ────────────────────────────────────────────
    # GLUCOSE
    # ────────────────────────────────────────────
    match = re.search(r'AVERAGE\s+BLOOD\s+GLUCOSE.*?CALCULATED\s+(\d+)\s*mg/dL', text_clean, re.DOTALL | re.IGNORECASE)
    if match:
        value = float(match.group(1))
        if 50 <= value <= 500:  # Sanity check
            tests.append({'name': 'Average Blood Glucose', 'value': value, 'unit': 'mg/dL', 'status': 'NORMAL'})
            print(f"   ✓ Average Blood Glucose = {value} mg/dL")
    
    print(f"\n   → Extracted {len(tests)} tests total")
    print(f"{'='*60}\n")
    
    return tests
# ============================================
# MAIN UPLOAD ENDPOINT
# ============================================
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
            return jsonify({'error': f'Invalid file type. Only {", ".join(ALLOWED_EXTENSIONS)} allowed'}), 400
        # Validate file size
        is_valid_size, file_size = validate_file_size(file)
        if not is_valid_size:
            return jsonify({
                'error': f'File too large. Maximum size is {MAX_FILE_SIZE/(1024*1024):.1f}MB',
                'file_size': f'{file_size/(1024*1024):.1f}MB'
            }), 400
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
        print(f"📄 FILE UPLOADED: {filename}")
        print(f"📏 Size: {file_size/(1024*1024):.1f}MB")
        print(f"{'='*60}")
        # ============================================
        # STEP 0.5: VERIFICATION (OPTIONAL)
        # ============================================
        verify_report_str = request.form.get('verify_report', 'false')
        verify_report = verify_report_str.lower() in ['true', '1', 'yes']
        print(f"🔍 Verification Toggle: {'ON' if verify_report else 'OFF'}")
        verification_result = None
        if verify_report:
            try:
                print("🔍 VERIFICATION ENABLED - Running forensics...")
                from utils.pdf_forensics import PDFForensics
              
                forensics = PDFForensics()
                verification_result = forensics.analyze_pdf(filepath)
              
                print(f"✅ Verification complete!")
                print(f" Trust Score: {verification_result['trust_score']}/100")
                print(f" Risk Level: {verification_result['risk_level']}")
              
            except Exception as e:
                print(f"❌ Verification failed: {e}")
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
            print("🔍 Verification: Skipped (toggle OFF)")
        # ============================================
        # STEP 1: EXTRACT TEXT
        # ============================================
        extracted_text = None
        extraction_method = None
      
        # Try PyPDF2 first (FASTEST) - ONLY for PDFs
        if filepath.lower().endswith('.pdf') and OCR_AVAILABLE and callable(process_file):
            try:
                print("🔄 Trying PyPDF2 (fast local extraction)...")
                extracted_text = process_file(filepath)
              
                # Check if text is meaningful (more than 50 chars)
                if extracted_text and len(extracted_text.strip()) > 50:
                    extraction_method = "PyPDF2 (local)"
                    print(f"✅ PyPDF2 SUCCESS! Extracted {len(extracted_text)} chars in <1 second")
                else:
                    # PyPDF2 returned empty/minimal text - likely scanned
                    print(f"⚠️ PyPDF2 returned minimal text ({len(extracted_text or '')} chars) - likely scanned PDF")
                    extracted_text = None # Reset to trigger AI fallback
            except Exception as e:
                print(f"❌ PyPDF2 failed: {e}")
                extracted_text = None
        # Fallback to Gemini AI OCR
        if not extracted_text:
            try:
                print("📸 PyPDF2 failed/insufficient text → Trying Gemini AI OCR...")
                from utils.ai_summarizer import extract_text_from_pdf_with_ai
              
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
        # Final validation
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
        # STEP 2: RULE-BASED ANALYSIS
        # ============================================
        rule_based_summary = None
        parsed_data = None
      
        if RULE_BASED_AVAILABLE and extracted_text:
            try:
                print("🧪 RUNNING RULE-BASED SYSTEM (YOUR CODE)...")
              
                # Parse the report
                parser = MedicalReportParser()
                parsed_data = parser.parse_report(
                    extracted_text,
                    gender="female", # TODO: Get from user profile
                    age=50 # TODO: Get from user profile
                )
              
                print(f"📊 Parsed {parsed_data['total_tests']} tests from report")
                print(f"📋 Report type: {parsed_data['report_type']}")
              
                # Generate summary using template system
                summarizer = TemplateSummarizer()
                rule_based_summary = summarizer.generate_summary(parsed_data)
              
                print(f"✅ RULE-BASED SUMMARY GENERATED! ({len(rule_based_summary)} chars)")
                print(f"{'='*60}\n")
              
            except Exception as e:
                print(f"❌ Rule-based system error: {e}")
                import traceback
                traceback.print_exc()
        # ============================================
        # STEP 2.5: MEDICAL VALIDATION
        # ============================================
        medical_validation = None
        if verify_report and parsed_data:
            try:
                print("⚕️ MEDICAL VALIDATION - Checking value plausibility...")
                from utils.medical_validator import MedicalValidator
              
                validator = MedicalValidator()
                medical_validation = validator.validate_report(parsed_data)
              
                print(f"✅ Medical validation complete!")
                print(f" Medical Suspicion: {medical_validation['suspicion_score']}")
              
                # Combine PDF forensics + medical validation
                if verification_result:
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
                  
                    print(f" Combined Trust Score: {verification_result['trust_score']}/100")
                    print(f" Final Risk Level: {verification_result['risk_level']}")
              
            except Exception as e:
                print(f"❌ Medical validation failed: {e}")
                import traceback
                traceback.print_exc()
        # ============================================
        # STEP 3: AI ENHANCEMENT
        # ============================================
        use_ai_str = request.form.get('use_ai', 'false')
        use_ai = use_ai_str.lower() in ['true', '1', 'yes']
        print(f"🤖 AI Enhancement Toggle: {'ON' if use_ai else 'OFF'}")
        ai_enhanced_summary = None
        ai_enhancement_success = False
        if use_ai and rule_based_summary:
            try:
                print("✨ AI ENHANCEMENT ENABLED - Polishing summary...")
                from utils.ai_summarizer import enhance_summary_with_ai
              
                ai_enhanced_summary = enhance_summary_with_ai(rule_based_summary)
              
                # Check if AI actually returned something different
                if ai_enhanced_summary and ai_enhanced_summary != rule_based_summary:
                    ai_enhancement_success = True
                    print(f"✅ AI enhancement SUCCESS!")
                else:
                    print(f"⚠️ AI enhancement returned same content (likely failed)")
                    ai_enhanced_summary = None
              
            except Exception as e:
                print(f"❌ AI enhancement failed: {e}")
                import traceback
                traceback.print_exc()
                ai_enhanced_summary = None
        # Use enhanced version if available AND successful
        final_summary = ai_enhanced_summary if ai_enhancement_success else rule_based_summary
        print(f"\n{'='*60}")
        print(f"📝 FINAL SUMMARY METHOD:")
        print(f" Using: {'AI Enhanced' if ai_enhancement_success else 'Rule-based Only'}")
        print(f" Length: {len(final_summary)} characters")
        print(f"{'='*60}\n")
        # ============================================
        # STEP 4: AI FALLBACK
        # ============================================
        ai_summary = None
        quick_summary = None
      
        if not rule_based_summary:
            print("🚨 Rule-based failed, using AI fallback...")
            try:
                from utils.ai_summarizer import generate_medical_summary, generate_quick_summary
                ai_summary = generate_medical_summary(extracted_text)
                quick_summary = generate_quick_summary(extracted_text)
                print("✅ AI summary generated (fallback)")
            except Exception as e:
                print(f"❌ AI summary also failed: {e}")
                return jsonify({'error': 'Summary generation failed completely'}), 500
        else:
            print("✅ Using rule-based summary")
            quick_summary = f"Analysis of {parsed_data['report_type']} - {parsed_data['total_tests']} tests analyzed"
        # ============================================
        # STEP 5: PREPARE FINAL SUMMARY
        # ============================================
      
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
        print(f"🎯 FINAL SUMMARY PREPARED")
        print(f"Method: {summary_data['method']}")
        print(f"Extraction: {extraction_method}")
        print(f"Tests found: {summary_data['tests_found']}")
        print(f"{'='*60}\n")
        # ============================================
        # STEP 6: SAVE TO DATABASE
        # ============================================
        reports_collection = current_app.db['reports']
        report_data = {
            'user_email': current_user,
            'filename': unique_filename,
            'original_filename': filename,
            'filepath': filepath,
            'file_size_mb': f'{file_size/(1024*1024):.2f}',
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
      
        print(f"💾 Saved to database - Report ID: {report_id}\n")
        # Update user's reports array
        users_collection = current_app.db['users']
        users_collection.update_one(
            {'email': current_user},
            {'$push': {'reports': report_id}}
        )
        return jsonify({
            'message': 'Report processed successfully',
            'report_id': report_id,
            'filename': filename,
            'file_size': f'{file_size/(1024*1024):.2f}MB',
            'summary': summary_data,
            'plain_language_summary': final_summary,
            'method_used': summary_data['method'],
            'extraction_method': extraction_method,
            'tests_analyzed': summary_data['tests_found'],
            'ai_enhanced': summary_data['ai_enhanced'],
            'verification_enabled': summary_data['verification_enabled']
        }), 200
    except Exception as e:
        print(f"\n❌ ERROR in upload_report:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup in case of errors during file processing
        pass
# ============================================
# HISTORY ENDPOINT
# ============================================
@report_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
        reports_collection = current_app.db['reports']
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
                'verification_enabled': report.get('verification_enabled', False),
                'file_size': report.get('file_size_mb', 'Unknown')
            })
        return jsonify({
            'message': 'History retrieved successfully',
            'total_reports': len(formatted_reports),
            'reports': formatted_reports
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# ============================================
# REPORT DETAILS ENDPOINT
# ============================================
@report_bp.route('/details/<report_id>', methods=['GET'])
@jwt_required()
def get_report_details(report_id):
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
        reports_collection = current_app.db['reports']
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
            'medical_validation': report.get('medical_validation'),
            'file_size': report.get('file_size_mb', 'Unknown')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
   
    # ============================================
# 🔥 ADD THIS TO YOUR report.py FILE 🔥
# ============================================
# Add this endpoint AFTER the /details/<report_id> endpoint (around line 500)
# This is the MISSING endpoint that your frontend is calling!
@report_bp.route('/verify-authenticity/<report_id>', methods=['GET'])
@jwt_required()
def verify_report_authenticity(report_id):
    """
    🔥 FIXED VERSION - Re-verify a report's authenticity
    This endpoint RE-PARSES the report with the FIXED parser
    and runs both PDF forensics and medical validation
    """
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
       
        current_user = get_jwt_identity()
       
        # Fetch the report from database
        reports_collection = current_app.db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
       
        if not report:
            return jsonify({'error': 'Report not found'}), 404
       
        print(f"\n{'='*60}")
        print(f"🔍 VERIFYING REPORT AUTHENTICITY")
        print(f"Report ID: {report_id}")
        print(f"User: {current_user}")
        print(f"Filename: {report.get('original_filename', 'Unknown')}")
        print(f"{'='*60}\n")
       
        filepath = report.get('filepath')
       
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'error': 'Report file not found',
                'details': 'The original PDF file is no longer available'
            }), 404
       
        # ============================================
        # STEP 1: PDF FORENSICS
        # ============================================
        verification_result = None
       
        try:
            print("🔍 Running PDF forensics...")
            from utils.pdf_forensics import PDFForensics
           
            forensics = PDFForensics()
            verification_result = forensics.analyze_pdf(filepath)
           
            print(f"✅ PDF Forensics complete!")
            print(f" Trust Score: {verification_result['trust_score']}/100")
            print(f" Risk Level: {verification_result['risk_level']}")
           
        except Exception as e:
            print(f"❌ PDF Forensics failed: {e}")
            import traceback
            traceback.print_exc()
            verification_result = {
                'verified': False,
                'trust_score': 0,
                'risk_level': 'Error',
                'suspicion_score': 100,
                'findings': [f'Verification error: {str(e)}'],
                'recommendations': ['Unable to verify - manual review required']
            }
       
        # ============================================
        # STEP 2: RE-PARSE WITH FIXED PARSER 🔧
        # ============================================
        parsed_data = None
       
        # Get OCR text (either from database or re-extract)
        extracted_text = report.get('extracted_text')
       
        if not extracted_text or len(extracted_text.strip()) < 50:
            print("⚠️ No OCR text in database, re-extracting...")
            # Re-extract if needed
            if OCR_AVAILABLE and callable(process_file):
                try:
                    extracted_text = process_file(filepath)
                except Exception as e:
                    print(f"❌ Text extraction failed: {e}")
                    extracted_text = None
       
        if extracted_text and len(extracted_text.strip()) >= 50:
            try:
                print("🧪 RE-PARSING REPORT WITH FIXED PARSER...")
               
                if not RULE_BASED_AVAILABLE:
                    raise Exception("Parser not available")
               
                from utils.report_parser import MedicalReportParser
               
                # 🔥 RE-PARSE with the FIXED parser
                parser = MedicalReportParser()
                parsed_data = parser.parse_report(
                    extracted_text,
                    gender=report.get('gender', 'female'), # Get from report if stored
                    age=report.get('age', 50) # Get from report if stored
                )
               
                print(f"✅ RE-PARSED: Found {parsed_data['total_tests']} tests")
                print(f"📋 Report type: {parsed_data['report_type']}")
               
                # 🔍 DEBUG: Print extracted values
                print(f"\n📊 EXTRACTED TEST VALUES:")
                for test in parsed_data.get('all_results', []):
                    print(f" • {test['term']}: {test['value']} {test['unit']}")
                print()
               
            except Exception as e:
                print(f"❌ Re-parsing failed: {e}")
                import traceback
                traceback.print_exc()
                # Use old parsed data if available
                parsed_data = report.get('parsed_data')
        else:
            print("⚠️ Using cached parsed_data from database")
            parsed_data = report.get('parsed_data')
       
        # ============================================
        # STEP 3: MEDICAL VALIDATION 🔧
        # ============================================
        medical_validation = None
       
        if parsed_data and parsed_data.get('all_results'):
            try:
                print("⚕️ MEDICAL VALIDATION - Checking value plausibility...")
                from utils.medical_validator import MedicalValidator
               
                validator = MedicalValidator()
                medical_validation = validator.validate_report(parsed_data)
               
                print(f"✅ Medical validation complete!")
                print(f" Medical Suspicion: {medical_validation['suspicion_score']}")
                print(f" Validated: {medical_validation['validated']}")
               
                # Combine PDF forensics + medical validation
                if verification_result:
                    pdf_suspicion = verification_result.get('suspicion_score', 0)
                    medical_suspicion = medical_validation['suspicion_score']
                    combined_suspicion = pdf_suspicion + medical_suspicion
                   
                    # Recalculate trust score
                    verification_result['trust_score'] = max(0, 100 - combined_suspicion)
                    verification_result['findings'].extend(medical_validation['findings'])
                    verification_result['medical_validation'] = medical_validation
                   
                    # Redetermine risk level based on combined score
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
                   
                    print(f"\n📊 FINAL RESULTS:")
                    print(f" PDF Suspicion: {pdf_suspicion}")
                    print(f" Medical Suspicion: {medical_suspicion}")
                    print(f" Combined Suspicion: {combined_suspicion}")
                    print(f" Trust Score: {verification_result['trust_score']}/100")
                    print(f" Risk Level: {verification_result['risk_level']}")
               
            except Exception as e:
                print(f"❌ Medical validation failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠️ No parsed data available for medical validation")
       
        # ============================================
        # STEP 4: UPDATE DATABASE WITH NEW RESULTS
        # ============================================
        try:
            # Update the report with new verification results
            update_data = {
                'verification': verification_result,
                'medical_validation': medical_validation,
                'last_verified_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p")
            }
           
            # Also update parsed_data if we re-parsed
            if parsed_data:
                update_data['parsed_data'] = parsed_data
           
            reports_collection.update_one(
                {'_id': ObjectId(report_id)},
                {'$set': update_data}
            )
           
            print(f"💾 Updated report in database")
           
        except Exception as e:
            print(f"⚠️ Failed to update database: {e}")
       
        print(f"{'='*60}\n")
       
        # ============================================
        # STEP 5: RETURN RESULTS
        # ============================================
        return jsonify({
            'success': True,
            'verification': verification_result,
            'medical_validation': medical_validation,
            'report_id': report_id,
            'verified_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p"),
            'parsed_data_available': parsed_data is not None,
            'tests_found': len(parsed_data.get('all_results', [])) if parsed_data else 0
        }), 200
       
    except Exception as e:
        print(f"\n❌ ERROR in verify_report_authenticity:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({
            'error': 'Verification failed',
            'details': str(e)
        }), 500
# ============================================
# 🔧 INSTRUCTIONS TO ADD THIS CODE:
# ============================================
"""
1. Open your backend/routes/report.py file
2. Find the line with:
   @report_bp.route('/details/<report_id>', methods=['GET'])
3. Scroll down to the END of that function (around line 500)
4. PASTE the entire verify_report_authenticity function above
5. Save the file
6. Restart your Flask server
7. Test by clicking "Verify Authenticity" on a report
That's it! The endpoint will now:
✅ Re-parse the report with the FIXED parser
✅ Run medical validation with correct values
✅ Show proper trust scores
"""
# ============================================
# 🔥 COMPARE TWO REPORTS 🔥 - FIXED WITH REGEX EXTRACTION
# ============================================
@report_bp.route('/compare', methods=['POST'])
@jwt_required()
def compare_reports():
    temp_files = []
    
    try:
        current_user = get_jwt_identity()
        
        if 'report1' not in request.files or 'report2' not in request.files:
            return jsonify({'error': 'Both reports are required'}), 400
        
        file1 = request.files['report1']
        file2 = request.files['report2']
        
        if not file1.filename or not file2.filename:
            return jsonify({'error': 'Both files must have filenames'}), 400
        
        if not (file1.filename.lower().endswith('.pdf') and file2.filename.lower().endswith('.pdf')):
            return jsonify({'error': 'Only PDF files are allowed for comparison'}), 400
        
        is_valid1, size1 = validate_file_size(file1)
        is_valid2, size2 = validate_file_size(file2)
        
        if not is_valid1 or not is_valid2:
            return jsonify({
                'error': 'One or both files exceed size limit',
                'max_size_mb': MAX_FILE_SIZE / (1024*1024),
                'report1_size_mb': size1 / (1024*1024),
                'report2_size_mb': size2 / (1024*1024)
            }), 400
        
        # Save temporarily
        upload_folder = os.path.join(os.getcwd(), 'uploads', 'temp')
        os.makedirs(upload_folder, exist_ok=True)
        
        timestamp = datetime.now(IST).strftime('%Y%m%d_%H%M%S')
        filename1 = secure_filename(f"temp1_{timestamp}_{file1.filename}")
        filename2 = secure_filename(f"temp2_{timestamp}_{file2.filename}")
        
        filepath1 = os.path.join(upload_folder, filename1)
        filepath2 = os.path.join(upload_folder, filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        temp_files = [filepath1, filepath2]
        
        print(f"\n{'='*60}")
        print("🔥 COMPARING REPORTS (REGEX MODE)")
        print(f"Report 1: {file1.filename}  ({size1/(1024*1024):.1f} MB)")
        print(f"Report 2: {file2.filename}  ({size2/(1024*1024):.1f} MB)")
        print(f"{'='*60}\n")
        
        # Text extraction
        start_time = time.time()
        
        text1 = extract_text_from_report_with_retry(filepath1, "Report 1")
        if not text1:
            return jsonify({'error': 'Could not extract text from Report 1'}), 400
            
        text2 = extract_text_from_report_with_retry(filepath2, "Report 2")
        if not text2:
            return jsonify({'error': 'Could not extract text from Report 2'}), 400
        
        print(f"Text extraction took {time.time() - start_time:.1f} seconds\n")
        
        # ────────────────────────────────────────────
        #  THE FIX: use regex instead of parser
        # ────────────────────────────────────────────
        print("Using direct REGEX extraction (bypassing MedicalReportParser)...\n")
        
        tests1 = extract_tests_from_raw_text(text1)
        print("\nDEBUG - REPORT 1 EXTRACTED TESTS:")
        for t in tests1:
            print(f"  - {t['name']}: {t['value']} {t['unit']}")
        
        tests2 = extract_tests_from_raw_text(text2)
        print("\nDEBUG - REPORT 2 EXTRACTED TESTS:")
        for t in tests2:
            print(f"  - {t['name']}: {t['value']} {t['unit']}")
        
        if len(tests1) == 0 or len(tests2) == 0:
            return jsonify({
                'error': 'No numerical test results detected in one or both reports',
                'report1_tests': len(tests1),
                'report2_tests': len(tests2)
            }), 400
        
        # Compare
        comparisons = compare_test_results(tests1, tests2)
        
        if len(comparisons) == 0:
            print("No exact matches → trying fuzzy matching...")
            comparisons = fuzzy_match_tests(tests1, tests2)
        
        if len(comparisons) == 0:
            return jsonify({
                'error': 'No matching tests found between the two reports',
                'report1_sample': [t['name'] for t in tests1[:6]],
                'report2_sample': [t['name'] for t in tests2[:6]]
            }), 400
        
        # Summary stats
        improved = worsened = stable = 0
        lower_is_better = {'cholesterol', 'ldl', 'triglycerides', 'glucose', 'hba1c',
                          'creatinine', 'urea', 'bilirubin', 'sgpt', 'sgot', 'alt', 'ast', 'vldl'}
        
        for comp in comparisons:
            delta = comp['change']
            name_lower = comp['name'].lower()
            is_lower_better = any(k in name_lower for k in lower_is_better)
            
            if abs(delta) < 0.01:
                stable += 1
                comp['status'] = 'stable'
            elif (delta < 0 and is_lower_better) or (delta > 0 and not is_lower_better):
                improved += 1
                comp['status'] = 'improved'
            else:
                worsened += 1
                comp['status'] = 'worsened'
        
        date1 = extract_date_from_text(text1)
        date2 = extract_date_from_text(text2)
        
        total_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'comparisons': comparisons,
            'summary': {
                'total_tests': len(comparisons),
                'improved_count': improved,
                'worsened_count': worsened,
                'stable_count': stable,
                'improvement_percentage': round((improved / len(comparisons) * 100), 1) if comparisons else 0
            },
            'report1_date': date1,
            'report2_date': date2,
            'report1_total_tests_found': len(tests1),
            'report2_total_tests_found': len(tests2),
            'report1_filename': file1.filename,
            'report2_filename': file2.filename,
            'processing_time_seconds': round(total_time, 1)
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
    finally:
        for path in temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
# ============================================
# 🔥 IMPROVED HELPER FUNCTIONS
# ============================================
def extract_text_from_report_with_retry(filepath, report_name, max_retries=2):
    """
    Extract text from a report with retry logic for transient failures
    """
    for attempt in range(max_retries):
        try:
            text = extract_text_from_report(filepath, report_name)
            if text and len(text.strip()) > 50:
                return text
        except Exception as e:
            print(f"⚠️ {report_name} Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying...")
                time.sleep(1) # Wait 1 second before retry
            else:
                print(f"❌ All {max_retries} attempts failed")
                return None
  
    return None
def extract_text_from_report(filepath, report_name):
    """
    Extract text from a report using PyPDF2 or AI fallback
    """
    text = None
  
    # Try PyPDF2 first (FAST - usually <1 second)
    if OCR_AVAILABLE and callable(process_file):
        try:
            print(f"🔄 {report_name}: Trying PyPDF2 (fast)...")
            start = time.time()
            text = process_file(filepath)
          
            if text and len(text.strip()) > 50:
                elapsed = time.time() - start
                print(f"✅ {report_name}: PyPDF2 success in {elapsed:.1f}s")
                return text
            else:
                print(f"⚠️ {report_name}: PyPDF2 returned minimal text")
        except Exception as e:
            print(f"❌ {report_name} PyPDF2 failed: {e}")
  
    # AI OCR fallback with timing
    try:
        print(f"🔄 {report_name}: Trying AI OCR (may take 10-30s for scanned PDFs)...")
        start = time.time()
      
        from utils.ai_summarizer import extract_text_from_pdf_with_ai
      
        text = extract_text_from_pdf_with_ai(filepath)
      
        elapsed = time.time() - start
      
        if text and len(text.strip()) >= 50:
            print(f"✅ {report_name}: AI OCR success in {elapsed:.1f}s")
            return text
        else:
            print(f"❌ {report_name}: AI OCR returned insufficient text")
            return None
          
    except Exception as e:
        print(f"❌ {report_name} AI OCR failed: {e}")
        return None
def extract_tests_from_parsed_data(parsed_data):
    """
    Extract test results from your MedicalReportParser output
    This converts your parser's format to the comparison format
    """
    tests = []
  
    if not parsed_data:
        return tests
  
    # Check if parsed_data has 'all_results'
    if 'all_results' in parsed_data:
        for test in parsed_data['all_results']:
            name = test.get('term', '')
            value = test.get('value')
            unit = test.get('unit', '')
          
            # Skip if no value
            if value is None or name == '':
                continue
          
            # Convert value to float
            try:
                if isinstance(value, str):
                    value = float(value.strip().replace(',', ''))
                else:
                    value = float(value)
            except (ValueError, AttributeError):
                continue
          
            tests.append({
                'name': name,
                'value': value,
                'unit': unit,
                'status': test.get('status', 'NORMAL')
            })
  
    # Fallback: Try categories structure
    elif 'categories' in parsed_data:
        for category_name, category_data in parsed_data.get('categories', {}).items():
            if isinstance(category_data, dict) and 'tests' in category_data:
                for test in category_data['tests']:
                    name = test.get('name', '')
                    value = test.get('value')
                    unit = test.get('unit', '')
                  
                    if value is None or name == '':
                        continue
                  
                    try:
                        if isinstance(value, str):
                            value = float(value.strip().replace(',', ''))
                        else:
                            value = float(value)
                    except (ValueError, AttributeError):
                        continue
                  
                    tests.append({
                        'name': name,
                        'value': value,
                        'unit': unit,
                        'status': test.get('status', 'NORMAL')
                    })
  
    return tests
def compare_test_results(tests1, tests2):
    """
    Compare two lists of test results and find matches
    """
    comparisons = []
  
    # Create lookup dictionaries (case-insensitive)
    tests1_dict = {test['name'].lower(): test for test in tests1}
    tests2_dict = {test['name'].lower(): test for test in tests2}
  
    # Find matches
    for name_lower in tests1_dict:
        if name_lower in tests2_dict:
            test1 = tests1_dict[name_lower]
            test2 = tests2_dict[name_lower]
          
            # Check if units match (case-insensitive)
            if test1['unit'].lower() == test2['unit'].lower():
                comparisons.append({
                    'name': test1['name'], # Use original case
                    'value1': test1['value'],
                    'value2': test2['value'],
                    'unit': test1['unit'],
                    'change': test2['value'] - test1['value'],
                    'percent_change': ((test2['value'] - test1['value']) / test1['value'] * 100) if test1['value'] != 0 else 0
                })
  
    return comparisons
def fuzzy_match_tests(tests1, tests2):
    """
    Find matching tests using fuzzy string matching
    For cases where test names are slightly different between reports
    """
    comparisons = []
    used_tests2 = set()
  
    for test1 in tests1:
        best_match = None
        best_ratio = 0.0
      
        for test2 in tests2:
            if test2['name'] in used_tests2:
                continue
          
            # Calculate similarity
            ratio = SequenceMatcher(None,
                                   test1['name'].lower(),
                                   test2['name'].lower()).ratio()
          
            # Check if units match and similarity is good
            if ratio > 0.75 and test1['unit'].lower() == test2['unit'].lower():
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = test2
      
        # If we found a match
        if best_match:
            comparisons.append({
                'name': test1['name'],
                'value1': test1['value'],
                'value2': best_match['value'],
                'unit': test1['unit'],
                'change': best_match['value'] - test1['value'],
                'percent_change': ((best_match['value'] - test1['value']) / test1['value'] * 100) if test1['value'] != 0 else 0,
                'match_confidence': best_ratio
            })
            used_tests2.add(best_match['name'])
  
    return comparisons
def extract_date_from_text(text):
    """
    Try to extract a date from the report text
    Returns ISO format date string or None
    """
    # Common date patterns
    date_patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', # DD/MM/YYYY or DD-MM-YYYY
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', # YYYY/MM/DD or YYYY-MM-DD
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})', # Month DD, YYYY
    ]
  
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                groups = match
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
                  
                    return date_obj.strftime("%Y-%m-%d")
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
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
      
        # Fetch the report
        reports_collection = current_app.db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
      
        if not report:
            return jsonify({'error': 'Report not found'}), 404
      
        # Get parsed data from report
        parsed_data = report.get('parsed_data', {})
      
        print(f"\n{'='*60}")
        print(f"🧮 CALCULATING HEALTH RISKS")
        print(f"Report ID: {report_id}")
        print(f"User: {current_user}")
        print(f"{'='*60}")
        print(f"Parsed data keys: {list(parsed_data.keys()) if parsed_data else 'NONE'}")
        print(f"{'='*60}\n")
      
        # Extract test values
        test_values = {}
      
        # METHOD 1: Try parsed_data['all_results'] (YOUR PARSER FORMAT!)
        if parsed_data and 'all_results' in parsed_data:
            tests = parsed_data['all_results']
            print(f"📋 METHOD 1: Found {len(tests)} tests in parsed_data['all_results']")
          
            for test in tests:
                test_name = str(test.get('term', '')).lower()
                test_value = test.get('value')
                test_unit = test.get('unit', '')
              
                print(f" Test: {test.get('term')} = {test_value} {test_unit}")
              
                if test_value is None:
                    continue
              
                try:
                    if isinstance(test_value, str):
                        test_value = test_value.strip().replace(',', '')
                        test_value = float(test_value)
                    else:
                        test_value = float(test_value)
                except Exception as e:
                    print(f" ❌ ERROR converting {test_value}: {e}")
                    continue
              
                # Map test names to standardized keys
                if 'total' in test_name and 'cholesterol' in test_name:
                    test_values['total_cholesterol'] = test_value
                    print(f" ✅ Mapped to: total_cholesterol")
                elif 'hdl' in test_name:
                    test_values['hdl'] = test_value
                    print(f" ✅ Mapped to: hdl")
                elif 'ldl' in test_name:
                    test_values['ldl'] = test_value
                    print(f" ✅ Mapped to: ldl")
                elif 'triglyceride' in test_name or 'trig' in test_name:
                    test_values['triglycerides'] = test_value
                    print(f" ✅ Mapped to: triglycerides")
                elif 'hba1c' in test_name or 'a1c' in test_name or ('hemoglobin' in test_name and 'a1c' in test_name):
                    test_values['hba1c'] = test_value
                    print(f" ✅ Mapped to: hba1c")
                elif 'glucose' in test_name:
                    test_values['fasting_glucose'] = test_value
                    print(f" ✅ Mapped to: fasting_glucose")
                elif 'creatinine' in test_name:
                    test_values['creatinine'] = test_value
                    print(f" ✅ Mapped to: creatinine")
                elif 'urea' in test_name or 'bun' in test_name:
                    test_values['urea'] = test_value
                    print(f" ✅ Mapped to: urea")
                else:
                    print(f" ⚠️ No mapping for this test")
      
        # METHOD 2: Try parsed_data['tests'] (fallback)
        elif parsed_data and 'tests' in parsed_data:
            tests = parsed_data['tests']
            print(f"📋 METHOD 2: Found {len(tests)} tests in parsed_data['tests']")
          
            for test in tests:
                test_name = str(test.get('name', '')).lower()
                test_value = test.get('value')
                test_unit = test.get('unit', '')
              
                print(f" Test: {test.get('name')} = {test_value} {test_unit}")
              
                if test_value is None:
                    continue
              
                try:
                    if isinstance(test_value, str):
                        test_value = test_value.strip().replace(',', '')
                        test_value = float(test_value)
                    else:
                        test_value = float(test_value)
                except Exception as e:
                    print(f" ❌ ERROR converting {test_value}: {e}")
                    continue
              
                # Same mapping logic
                if 'total' in test_name and 'cholesterol' in test_name:
                    test_values['total_cholesterol'] = test_value
                elif 'hdl' in test_name:
                    test_values['hdl'] = test_value
                elif 'ldl' in test_name:
                    test_values['ldl'] = test_value
                elif 'triglyceride' in test_name:
                    test_values['triglycerides'] = test_value
                elif 'hba1c' in test_name or 'a1c' in test_name:
                    test_values['hba1c'] = test_value
                elif 'glucose' in test_name:
                    test_values['fasting_glucose'] = test_value
                elif 'creatinine' in test_name:
                    test_values['creatinine'] = test_value
                elif 'urea' in test_name or 'bun' in test_name:
                    test_values['urea'] = test_value
      
        # METHOD 3: Try categories structure
        if not test_values and parsed_data and 'categories' in parsed_data:
            print(f"📋 METHOD 3: Trying categories structure")
            categories = parsed_data['categories']
            print(f" Found categories: {list(categories.keys())}")
          
            for category_name, category_data in categories.items():
                if isinstance(category_data, dict) and 'tests' in category_data:
                    print(f" Category '{category_name}' has {len(category_data['tests'])} tests")
                    for test in category_data['tests']:
                        test_name = str(test.get('name', '')).lower()
                        test_value = test.get('value')
                      
                        if test_value is None:
                            continue
                      
                        try:
                            if isinstance(test_value, str):
                                test_value = float(test_value.strip().replace(',', ''))
                            else:
                                test_value = float(test_value)
                        except:
                            continue
                      
                        # Same mapping logic
                        if 'total' in test_name and 'cholesterol' in test_name:
                            test_values['total_cholesterol'] = test_value
                        elif 'hdl' in test_name:
                            test_values['hdl'] = test_value
                        elif 'ldl' in test_name:
                            test_values['ldl'] = test_value
                        elif 'triglyceride' in test_name:
                            test_values['triglycerides'] = test_value
                        elif 'hba1c' in test_name or 'a1c' in test_name:
                            test_values['hba1c'] = test_value
                        elif 'glucose' in test_name:
                            test_values['fasting_glucose'] = test_value
                        elif 'creatinine' in test_name:
                            test_values['creatinine'] = test_value
                        elif 'urea' in test_name:
                            test_values['urea'] = test_value
      
        print(f"\n{'='*60}")
        print(f"📊 FINAL EXTRACTED TEST VALUES:")
        for key, value in test_values.items():
            print(f" {key}: {value}")
        print(f"{'='*60}\n")
      
        # Check if we have any test values
        if not test_values:
            return jsonify({
                'error': 'No test data available for risk calculation',
                'details': 'Could not find required test values in the report.',
                'debug': {
                    'parsed_data_keys': list(parsed_data.keys()) if parsed_data else [],
                    'has_all_results': 'all_results' in parsed_data if parsed_data else False,
                    'has_tests_key': 'tests' in parsed_data if parsed_data else False,
                    'has_categories_key': 'categories' in parsed_data if parsed_data else False
                }
            }), 400
      
        # Calculate risks
        risks = calculate_all_risks(test_values)
      
        return jsonify({
            'success': True,
            'risks': risks,
            'test_values_found': test_values,
            'report_id': report_id,
            'calculated_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p")
        }), 200
      
    except Exception as e:
        print(f"\n❌ ERROR in calculate_health_risks:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e), 'type': 'exception'}), 500
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
            risk_points -= 1 # Protective factor
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
        if creatinine > 1.3: # Elevated for most adults
            risk_points += 2
            risk['factors'].append(f'Elevated Creatinine: {creatinine} mg/dL (>1.3)')
        elif creatinine > 1.1:
            risk_points += 1
            risk['factors'].append(f'Borderline Creatinine: {creatinine} mg/dL (>1.1)')
        else:
            risk['factors'].append(f'Normal Creatinine: {creatinine} mg/dL (<=1.1)')
  
    # Urea assessment
    if urea is not None:
        if urea > 45: # Elevated
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
# ============================================
# 🔥 DIET RECOMMENDATIONS ENDPOINT 🔥
# ============================================
@report_bp.route('/diet-recommendations/<report_id>', methods=['GET'])
@jwt_required()
def get_diet_recommendations(report_id):
    """
    Generate personalized diet recommendations based on report
    Returns comprehensive diet plan
    """
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
      
        # Fetch the report
        reports_collection = current_app.db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
      
        if not report:
            return jsonify({'error': 'Report not found'}), 404
      
        # Get parsed data from report
        parsed_data = report.get('parsed_data', {})
      
        if not parsed_data:
            return jsonify({
                'error': 'No test data available',
                'details': 'Report must be processed to generate diet recommendations'
            }), 400
      
        print(f"\n{'='*60}")
        print(f"🍎 GENERATING DIET RECOMMENDATIONS")
        print(f"Report ID: {report_id}")
        print(f"User: {current_user}")
        print(f"{'='*60}\n")
      
        # Import the diet recommender
        try:
            import sys
            import os
            utils_path = os.path.join(os.path.dirname(__file__), '..', 'utils')
            if utils_path not in sys.path:
                sys.path.insert(0, utils_path)
          
            from diet_recommender import generate_diet_recommendations
          
            # Generate diet plan
            diet_plan = generate_diet_recommendations(parsed_data)
          
            print(f"✅ Diet plan generated successfully!")
            print(f"📋 Conditions detected: {diet_plan.get('conditions_detected', [])}")
            print(f"{'='*60}\n")
          
            # Save diet plan to report
            reports_collection.update_one(
                {'_id': ObjectId(report_id)},
                {'$set': {'diet_recommendations': diet_plan}}
            )
          
            return jsonify({
                'success': True,
                'diet_plan': diet_plan,
                'report_id': report_id,
                'generated_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p")
            }), 200
          
        except ImportError as e:
            print(f"❌ Failed to import diet recommender: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Diet recommendation system unavailable',
                'details': str(e)
            }), 500
        except Exception as e:
            print(f"❌ Diet generation error: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Failed to generate diet recommendations',
                'details': str(e)
            }), 500
      
    except Exception as e:
        print(f"\n❌ ERROR in get_diet_recommendations:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e), 'type': 'exception'}), 500
  
# ============================================
# 🔥 CHAT WITH REPORT ENDPOINT 🔥
# ============================================
@report_bp.route('/chat/<report_id>', methods=['POST'])
@jwt_required()
def chat_with_report(report_id):
    """
    Chat with AI about the medical report
    Provides context-aware answers based on report data
    """
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
      
        # Get user's question and chat history
        data = request.get_json()
        user_question = data.get('question', '').strip()
        chat_history = data.get('history', []) # List of {role, content}
      
        if not user_question:
            return jsonify({'error': 'Question is required'}), 400
      
        # Fetch the report
        reports_collection = current_app.db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
      
        if not report:
            return jsonify({'error': 'Report not found'}), 404
      
        print(f"\n{'='*60}")
        print(f"💬 CHAT WITH REPORT")
        print(f"Report ID: {report_id}")
        print(f"Question: {user_question}")
        print(f"History length: {len(chat_history)}")
        print(f"{'='*60}\n")
      
        # Get report data
        plain_summary = report.get('plain_language_summary', '')
        parsed_data = report.get('parsed_data', {})
        extracted_text = report.get('extracted_text', '')
      
        # Build context for AI
        try:
            import requests
            import os
          
            # Use REST API with correct model
            GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
          
            headers = {"Content-Type": "application/json"}
          
            # Build comprehensive context
            context = f"""You are a helpful medical assistant analyzing a patient's medical report.
REPORT SUMMARY:
{plain_summary}
AVAILABLE TEST DATA:
"""
          
            # Add test results if available
            if parsed_data and 'all_results' in parsed_data:
                context += "\nTest Results:\n"
                for test in parsed_data['all_results'][:20]: # Limit to first 20 tests
                    term = test.get('term', '')
                    value = test.get('value', '')
                    unit = test.get('unit', '')
                    status = test.get('status', '')
                    if term and value:
                        context += f"- {term}: {value} {unit} ({status})\n"
          
            context += f"""
INSTRUCTIONS:
1. Answer the user's question based on the report data above
2. Be clear, accurate, and helpful
3. Cite specific test values when relevant
4. Use simple language, avoid medical jargon unless necessary
5. If the report doesn't contain info to answer the question, say so politely
6. Add disclaimers when giving medical advice
7. Keep responses concise but informative
USER QUESTION: {user_question}
Provide a helpful, accurate answer:"""
          
            # Build conversation history for context
            conversation = []
            for msg in chat_history[-6:]: # Keep last 6 messages for context
                conversation.append(f"{msg['role'].upper()}: {msg['content']}")
          
            if conversation:
                context = "CONVERSATION HISTORY:\n" + "\n".join(conversation) + "\n\n" + context
          
            # Generate response using REST API
            print("🤖 Generating AI response...")
          
            payload = {
                "contents": [{
                    "parts": [{"text": context}]
                }]
            }
          
            response = requests.post(url, headers=headers, json=payload, timeout=30)
          
            if response.status_code == 200:
                result = response.json()
                ai_answer = result['candidates'][0]['content']['parts'][0]['text']
              
                print(f"✅ AI Response generated ({len(ai_answer)} chars)")
                print(f"{'='*60}\n")
              
                return jsonify({
                    'success': True,
                    'answer': ai_answer,
                    'question': user_question,
                    'timestamp': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p")
                }), 200
            else:
                error_detail = response.json() if response.text else response.text
                raise Exception(f"Gemini API Error {response.status_code}: {error_detail}")
          
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Failed to generate response',
                'details': str(e)
            }), 500
      
    except Exception as e:
        print(f"\n❌ ERROR in chat_with_report:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e)}), 500
@report_bp.route('/chat/suggestions/<report_id>', methods=['GET'])
@jwt_required()
def get_chat_suggestions(report_id):
    """
    Get smart suggested questions based on the report
    """
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
      
        # Fetch the report
        reports_collection = current_app.db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
      
        if not report:
            return jsonify({'error': 'Report not found'}), 404
      
        # Get parsed data
        parsed_data = report.get('parsed_data', {})
      
        # Build smart suggestions based on report
        suggestions = [
            "Can you explain my test results in simple terms?",
            "What do my abnormal values mean?",
            "What should I do to improve my health?"
        ]
      
        # Add condition-specific suggestions
        if parsed_data and 'all_results' in parsed_data:
            abnormal_tests = [t for t in parsed_data['all_results'] if t.get('status') in ['HIGH', 'LOW', 'CRITICAL']]
          
            if abnormal_tests:
                # Add specific questions about abnormal tests
                for test in abnormal_tests[:2]: # First 2 abnormal tests
                    term = test.get('term', '')
                    if term:
                        suggestions.append(f"Why is my {term} abnormal?")
              
                suggestions.append("What foods should I eat based on my results?")
                suggestions.append("Are these results concerning?")
      
        # Limit to 6 suggestions
        suggestions = suggestions[:6]
      
        return jsonify({
            'success': True,
            'suggestions': suggestions
        }), 200
      
    except Exception as e:
        print(f"❌ ERROR in get_chat_suggestions: {e}")
        return jsonify({'error': str(e)}), 500
# ============================================
# DELETE REPORT ENDPOINT
# ============================================
@report_bp.route('/delete/<report_id>', methods=['DELETE'])
@jwt_required()
def delete_report(report_id):
    """
    Delete a report and its associated file
    """
    try:
        if not BSON_AVAILABLE:
            return jsonify({'error': 'Database features unavailable'}), 500
          
        current_user = get_jwt_identity()
      
        # Fetch the report
        reports_collection = current_app.db['reports']
        report = reports_collection.find_one({
            '_id': ObjectId(report_id),
            'user_email': current_user
        })
      
        if not report:
            return jsonify({'error': 'Report not found'}), 404
      
        # Delete the file from uploads folder
        filepath = report.get('filepath')
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🗑️ Deleted file: {filepath}")
            except Exception as e:
                print(f"⚠️ Failed to delete file {filepath}: {e}")
      
        # Delete from database
        result = reports_collection.delete_one({'_id': ObjectId(report_id)})
      
        # Remove from user's reports array
        users_collection = current_app.db['users']
        users_collection.update_one(
            {'email': current_user},
            {'$pull': {'reports': report_id}}
        )
      
        return jsonify({
            'success': True,
            'message': 'Report deleted successfully',
            'report_id': report_id
        }), 200
      
    except Exception as e:
        print(f"\n❌ ERROR in delete_report:")
        print(f"{'='*60}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return jsonify({'error': str(e)}), 500