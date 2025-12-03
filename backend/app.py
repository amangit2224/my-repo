from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import os
import sys

# FIX: Allow imports from backend root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# Create uploads folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Import routes
from routes.auth import auth_bp
from routes.report import report_bp
from routes.jargon import jargon_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(report_bp, url_prefix='/api/report')
app.register_blueprint(jargon_bp, url_prefix='/api/jargon')

@app.route('/')
def home():
    return {'message': 'API is running!', 'status': 'success'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)