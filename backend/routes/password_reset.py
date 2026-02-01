from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from models.user import User
from utils.token_utils import generate_token
from utils.email_service import send_reset_email
import os
import re

password_reset_bp = Blueprint("password_reset", __name__)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@password_reset_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(force=True)
    email = data.get("email", "").strip().lower()

    response_msg = "Reset link sent successfully"

    if not email or not EMAIL_REGEX.match(email):
        return jsonify({"message": response_msg}), 200

    user = current_app.db['users'].find_one({"email": email})
    if not user:
        return jsonify({"message": response_msg}), 200

    token = generate_token()

    current_app.db['password_resets'].insert_one({
        "email": email,
        "token": token,
        "expires_at": datetime.utcnow() + timedelta(hours=1),
        "used": False,
        "created_at": datetime.utcnow()
    })

    frontend_url = os.getenv("FRONTEND_URL")
    reset_link = f"{frontend_url}/reset-password?token={token}"

    send_reset_email(email, reset_link)

    return jsonify({"message": response_msg}), 200

@password_reset_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(force=True)

    token = data.get("token")
    password = data.get("password")

    if not token or not password:
        return jsonify({"error": "Invalid request"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    record = current_app.db['password_resets'].find_one({
        "token": token,
        "used": False,
        "expires_at": {"$gt": datetime.utcnow()}
    })

    if not record:
        return jsonify({"error": "Invalid or expired link"}), 400

    hashed_password = User.hash_password(password)

    current_app.db['users'].update_one(
        {"email": record["email"]},
        {"$set": {"password_hash": hashed_password}}
    )

    current_app.db['password_resets'].update_one(
        {"_id": record["_id"]},
        {"$set": {"used": True}}
    )

    print(f"Password reset successful for: {record['email']}")

    return jsonify({"message": "Password reset successful"}), 200