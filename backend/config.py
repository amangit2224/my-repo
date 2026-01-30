import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Database
    MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/medical_report_db')
    
    # File Upload
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    
    # Frontend URL for CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')