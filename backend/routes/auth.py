from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from app import db                # ← IMPORT db FROM app.py (NO localhost!)
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email    = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        users_collection = db['users']

        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already registered'}), 400
        if users_collection.find_one({'username': username}):
            return jsonify({'error': 'Username already taken'}), 400

        new_user = User(username, email, password)
        users_collection.insert_one(new_user.to_dict())

        return jsonify({'message': 'User registered successfully', 'username': username}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email    = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        users_collection = db['users']
        user = users_collection.find_one({'email': email})

        if not user or not User.check_password(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401

        access_token = create_access_token(identity=email)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'username': user['username']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500