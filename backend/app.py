import os
import sys
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config

# Load environment variables
load_dotenv()

# Allow imports from backend root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# ✅ FIXED CORS (THIS IS THE KEY FIX)
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True
)

jwt = JWTManager(app)

# MongoDB Connection
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client.get_database()
    print("Connected to MongoDB successfully")
except Exception as e:
    print("MongoDB connection failed:", e)
    sys.exit(1)

# Attach db to app
app.db = db

# Create uploads folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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

# ✅ FIX: Explicit OPTIONS handler for preflight
@app.route('/api/<path:path>', methods=['OPTIONS'])
def api_options(path):
    return '', 200

@app.route('/')
def home():
    return {
        'message': 'Medical Report Summarizer API is running',
        'status': 'success'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
