import os
import sys
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from config import Config

# Load environment variables
load_dotenv()

# Allow imports from backend root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# ✅ CORS - Allow your Vercel frontend
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# ✅ RATE LIMITING - Prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

jwt = JWTManager(app)

# MongoDB Connection
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client.get_database()
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

# Attach db to app
app.db = db

# Create uploads folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import blueprints AFTER app creation
from routes.auth import auth_bp
from routes.report import report_bp
from routes.jargon import jargon_bp
from routes.password_reset import password_reset_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(report_bp, url_prefix='/api/report')
app.register_blueprint(jargon_bp, url_prefix='/api/jargon')
app.register_blueprint(password_reset_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        'message': 'Medical Report Summarizer API',
        'status': 'active',
        'version': '2.0',
        'disclaimer': 'Educational use only. Not for medical diagnosis or treatment.'
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'medical-report-api'
    })

@app.route('/api/disclaimer')
def get_disclaimer():
    return jsonify({
        'disclaimer': '''⚠️ IMPORTANT MEDICAL DISCLAIMER
        
This application is an educational tool for demonstration purposes only.

- NOT a substitute for professional medical advice, diagnosis, or treatment
- Always consult qualified healthcare professionals for medical concerns
- Do not rely solely on this tool for health decisions
- Summaries are AI-generated and may contain errors
- Emergency? Call your local emergency services immediately

By using this service, you acknowledge these limitations.'''
    })

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong. Please try again later.'
    }), 500

if __name__ == '__main__':
    # Local development only - Railway uses Gunicorn
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))