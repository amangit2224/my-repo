from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
import os
from datetime import datetime
from pytz import timezone

IST = timezone('Asia/Kolkata')
report_bp = Blueprint('report', __name__)

# ============================================
# IMPORT YOUR RULE-BASED SYSTEM 🔥
# ============================================
try:
    from utils.report_parser import MedicalReportParser
    from utils.template_summarizer import TemplateSummarizer
    RULE_BASED_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Rule-based system not available: {e}")
    RULE_BASED_AVAILABLE = False

# Try to import local OCR helper
try:
    from utils.ocr import process_file
except Exception:
    process_file = None

# AI summarizer helpers
def ai_extract_text_fallback(filepath):
    """AI-based PDF/text extractor fallback"""
    try:
        from utils.ai_summarizer import extract_text_from_pdf, extract_text_from_file
        if 'extract_text_from_pdf' in locals():
            try:
                return extract_text_from_pdf(filepath)
            except Exception:
                pass
        try:
            return extract_text_from_file(filepath)
        except Exception:
            pass
    except Exception:
        try:
            from utils.ai_summarizer import extract_text
            return extract_text(filepath)
        except Exception:
            return None
    return None


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

        # ============================================
        # STEP 1: EXTRACT TEXT
        # ============================================
        extracted_text = None
        
        # Try local OCR first
        if callable(process_file):
            extracted_text = process_file(filepath)

        # Fallback to AI text extraction
        if not extracted_text:
            try:
                from utils.ai_summarizer import extract_text_from_pdf_with_ai
                extracted_text = extract_text_from_pdf_with_ai(filepath)
            except Exception as e:
                return jsonify({'error': f'Text extraction failed: {str(e)}'}), 500

        # ============================================
        # STEP 2: RULE-BASED ANALYSIS (YOUR CODE!) 🔥
        # ============================================
        rule_based_summary = None
        parsed_data = None
        
        if RULE_BASED_AVAILABLE and extracted_text:
            try:
                print("🔥 Using RULE-BASED system (YOUR CODE)...")
                
                # Parse the report
                parser = MedicalReportParser()
                parsed_data = parser.parse_report(
                    extracted_text, 
                    gender="female",  # TODO: Get from user profile
                    age=50  # TODO: Get from user profile
                )
                
                # Generate summary using YOUR template system
                summarizer = TemplateSummarizer()
                rule_based_summary = summarizer.generate_summary(parsed_data)
                
                print(f"✅ Rule-based summary generated! ({len(rule_based_summary)} chars)")
                
            except Exception as e:
                print(f"⚠️  Rule-based system failed: {e}")
                # Continue to AI fallback

        # ============================================
        # STEP 3: AI SUMMARY (OPTIONAL/FALLBACK)
        # ============================================
        ai_summary = None
        quick_summary = None
        
        try:
            from utils.ai_summarizer import generate_medical_summary, generate_quick_summary
            
            # Only use AI if rule-based failed OR as enhancement
            if not rule_based_summary:
                print("⚠️  Using AI summary (fallback)...")
                ai_summary = generate_medical_summary(extracted_text)
                quick_summary = generate_quick_summary(extracted_text)
            else:
                print("✅ Rule-based summary primary, AI skipped (optional)")
                # Optionally: Use AI to polish the rule-based summary
                # ai_summary = generate_medical_summary(rule_based_summary)
                
        except Exception as e:
            print(f"⚠️  AI summary failed: {e}")
            # Not critical if rule-based worked

        # ============================================
        # STEP 4: PREPARE FINAL SUMMARY
        # ============================================
        
        # Use rule-based as primary, AI as fallback
        final_summary = rule_based_summary if rule_based_summary else ai_summary
        
        if not final_summary:
            return jsonify({'error': 'Summary generation failed'}), 500

        summary_data = {
            'plain_language_summary': final_summary,
            'quick_summary': quick_summary if quick_summary else "Summary generated using rule-based system",
            'status': 'success',
            'word_count': len(extracted_text.split()),
            'method': 'rule_based' if rule_based_summary else 'ai_fallback',
            'tests_found': parsed_data['total_tests'] if parsed_data else 0,
            'report_type': parsed_data['report_type'] if parsed_data else 'Unknown'
        }

        # ============================================
        # STEP 5: SAVE TO DATABASE
        # ============================================
        reports_collection = db['reports']

        report_data = {
            'user_email': current_user,
            'filename': unique_filename,
            'original_filename': filename,
            'filepath': filepath,
            'extracted_text': extracted_text,
            'summary': summary_data,
            'plain_language_summary': final_summary,
            'rule_based_summary': rule_based_summary,
            'ai_summary': ai_summary,
            'parsed_data': parsed_data,  # Store parsed medical values
            'uploaded_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p"),
            'processed': True
        }

        result = reports_collection.insert_one(report_data)

        # Update user's reports array
        users_collection = db['users']
        users_collection.update_one(
            {'email': current_user},
            {'$push': {'reports': str(result.inserted_id)}}
        )

        return jsonify({
            'message': 'Report processed successfully',
            'report_id': str(result.inserted_id),
            'filename': filename,
            'summary': summary_data,
            'plain_language_summary': final_summary,
            'method_used': summary_data['method'],
            'tests_analyzed': summary_data['tests_found']
        }), 200

    except Exception as e:
        print(f"❌ Error in upload_report: {e}")
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
                'report_type': report.get('summary', {}).get('report_type', 'Unknown')
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
            'parsed_data': report.get('parsed_data'),  # Include parsed medical values
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500