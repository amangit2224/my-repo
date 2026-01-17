from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config
from dotenv import load_dotenv
load_dotenv()
import os
import sys
from routes.password_reset import password_reset_bp
app.register_blueprint(password_reset_bp)

# FIX: Allow imports from backend root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with proper CORS config
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

jwt = JWTManager(app)

# ──────────────────────────────────────
# MongoDB Connection using .env variable
# ──────────────────────────────────────
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client.get_database()  # automatically picks the database from the URI
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)
    sys.exit(1)  # stop the app if DB is down
# ──────────────────────────────────────

# Create uploads folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Import routes (they will use the `db` object from above)
from routes.auth import auth_bp
from routes.report import report_bp
from routes.jargon import jargon_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(report_bp, url_prefix='/api/report')
app.register_blueprint(jargon_bp, url_prefix='/api/jargon')

@app.route('/')
def home():
    return {'message': 'Medical Report Summarizer API is running', 'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)