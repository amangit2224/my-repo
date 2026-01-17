from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from utils.token_utils import generate_token, hash_token
from utils.email_service import send_test_email  # temporary
from database import db
import os
import re
from werkzeug.security import generate_password_hash

password_reset_bp = Blueprint("password_reset", __name__)

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@password_reset_bp.route("/api/forgot-password", methods=["POST"])
def forgot_password():
    email = request.json.get("email", "").strip().lower()
    
    # Validate email format
    if not email or not EMAIL_REGEX.match(email):
        return jsonify({"message": "If the email exists, a reset link will be sent."}), 200
    
    user = db.users.find_one({"email": email})
    if user:
        # Check for recent requests to prevent spam
        recent_request = db.password_resets.find_one({
            "email": email,
            "created_at": {"$gt": datetime.utcnow() - timedelta(minutes=15)},
            "used": False
        })
        
        if recent_request:
            return jsonify({"message": "If the email exists, a reset link will be sent."}), 200
        
        token = generate_token()
        token_hash = hash_token(token)
        
        db.password_resets.insert_one({
            "email": email,
            "token_hash": token_hash,
            "expires_at": datetime.utcnow() + timedelta(hours=1),
            "used": False,
            "created_at": datetime.utcnow()
        })
        
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        reset_link = f"{frontend_url}/reset-password?token={token}"
        
        # In production, use proper email with reset_link
        send_test_email(email)  # TEMP: Should include reset_link
        
        # Log the request (optional)
        print(f"Password reset requested for: {email}")
    
    return jsonify({"message": "If the email exists, a reset link will be sent."}), 200

@password_reset_bp.route("/api/reset-password", methods=["POST"])
def reset_password():
    token = request.json.get("token", "").strip()
    password = request.json.get("password", "").strip()
    
    # Validate inputs
    if not token:
        return jsonify({"error": "Token is required"}), 400
    
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    
    token_hash = hash_token(token)
    
    record = db.password_resets.find_one({
        "token_hash": token_hash,
        "used": False,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not record:
        return jsonify({"error": "Invalid or expired link"}), 400
    
    # Check if user still exists
    user = db.users.find_one({"email": record["email"]})
    if not user:
        return jsonify({"error": "User not found"}), 400
    
    # Update password
    db.users.update_one(
        {"email": record["email"]},
        {"$set": {"password": generate_password_hash(password)}}
    )
    
    # Mark token as used
    db.password_resets.update_one(
        {"_id": record["_id"]},
        {"$set": {"used": True, "used_at": datetime.utcnow()}}
    )
    
    # Invalidate all other reset tokens for this user
    db.password_resets.update_many(
        {"email": record["email"], "used": False},
        {"$set": {"used": True, "invalidated_at": datetime.utcnow()}}
    )
    
    return jsonify({"message": "Password reset successful"}), 200