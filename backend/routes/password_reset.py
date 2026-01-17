from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from utils.token_utils import generate_token, hash_token
from utils.email_service import send_reset_email
from database import db
import os
import re

password_reset_bp = Blueprint("password_reset", __name__)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# ─────────────────────────────
# FORGOT PASSWORD
# ─────────────────────────────
@password_reset_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email", "").strip().lower()

    # Always return same response (security)
    response_msg = "Reset link sent successfully"

    if not email or not EMAIL_REGEX.match(email):
        return jsonify({"message": response_msg}), 200

    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"message": response_msg}), 200

    token = generate_token()
    token_hash = hash_token(token)

    db.password_resets.insert_one({
        "email": email,
        "token_hash": token_hash,
        "expires_at": datetime.utcnow() + timedelta(hours=1),
        "used": False,
        "created_at": datetime.utcnow()
    })

    frontend_url = os.getenv("FRONTEND_URL")
    reset_link = f"{frontend_url}/reset-password?token={token}"

    send_reset_email(email, reset_link)

    return jsonify({"message": response_msg}), 200


# ─────────────────────────────
# RESET PASSWORD
# ─────────────────────────────
@password_reset_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token", "").strip()
    password = data.get("password", "").strip()

    if not token:
        return jsonify({"error": "Invalid token"}), 400

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

    db.users.update_one(
        {"email": record["email"]},
        {"$set": {"password": generate_password_hash(password)}}
    )

    db.password_resets.update_one(
        {"_id": record["_id"]},
        {"$set": {"used": True}}
    )

    return jsonify({"message": "Password reset successful"}), 200
