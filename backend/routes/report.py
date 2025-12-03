from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from database import db
from utils.ocr import process_file
from utils.nlp_processor import summarize_report, create_plain_language_summary
import os
from datetime import datetime
from pytz import timezone  

# ADD TIMEZONE SETUP
IST = timezone('Asia/Kolkata')

report_bp = Blueprint('report', __name__)

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
        timestamp = datetime.now(IST).strftime('%Y%m%d_%H%M%S')  # CHANGED THIS LINE
        unique_filename = f"{timestamp}_{filename}"

        # Create uploads folder if not exists
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)

        # Process OCR - Extract text from file
        extracted_text = process_file(filepath)

        # Process AI - Generate intelligent summary
        try:
            from utils.ai_summarizer import generate_medical_summary, generate_quick_summary

            print("Generating AI summary...")
            plain_summary = generate_medical_summary(extracted_text)
            quick_summary = generate_quick_summary(extracted_text)

            summary = {
                'plain_language_summary': plain_summary,
                'quick_summary': quick_summary,
                'status': 'success',
                'word_count': len(extracted_text.split())
            }

        except Exception as e:
            return jsonify({'error': f'AI processing failed: {str(e)}'}), 500

        # Save report to database
        reports_collection = db['reports']

        report_data = {
            'user_email': current_user,
            'filename': unique_filename,
            'original_filename': filename,
            'filepath': filepath,
            'extracted_text': extracted_text,
            'summary': summary,
            'plain_language_summary': plain_summary,
            'uploaded_at': datetime.now(IST).strftime("%Y-%m-%d %I:%M %p"),  # CHANGED THIS LINE
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
            'summary': summary,
            'plain_language_summary': plain_summary
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        current_user = get_jwt_identity()

        # Fetch user's reports
        reports_collection = db['reports']
        reports = list(reports_collection.find(
            {'user_email': current_user}
        ).sort('uploaded_at', -1))

        # Convert ObjectId to string and format response
        formatted_reports = []
        for report in reports:
            formatted_reports.append({
                'id': str(report['_id']),
                'filename': report.get('original_filename', 'Unknown'),
                'uploaded_at': report.get('uploaded_at'),  # CHANGED THIS LINE - already formatted
                'plain_summary': report.get('plain_language_summary', 'No summary available')
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
            'uploaded_at': report.get('uploaded_at'),  # CHANGED THIS LINE - already formatted
            'extracted_text': report.get('extracted_text'),
            'summary': report.get('summary'),
            'plain_language_summary': report.get('plain_language_summary')
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500