from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data or 'full_name' not in data:
        return jsonify({"error": "Missing email, password, or full_name"}), 400
    
    response, status_code = AuthService.sign_up(
        email=data['email'],
        password=data['password'],
        full_name=data['full_name']
    )
    return jsonify(response), status_code

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400
    
    response, status_code = AuthService.sign_in(
        email=data['email'],
        password=data['password']
    )
    return jsonify(response), status_code
