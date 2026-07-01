import sys
import os
from flask import Blueprint, jsonify, request
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from backend.services.diet_service import DietService

diet_bp = Blueprint('diet', __name__)

@diet_bp.route('/generate', methods=['POST'])
def generate_goal_diet():
    data = request.get_json()
    if not data or 'goal' not in data:
        return jsonify({"error": "Goal is required"}), 400

    try:
        result = DietService.generate_goal_based_diet(data)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@diet_bp.route('/', methods=['GET'])
@token_required
def get_user_diet(current_user):
    result = DietService.get_recommendations(current_user.get('sub'))
    return jsonify(result), 200
