import sys
import os
from flask import Blueprint, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from services.bmi_service import BMIService

bmi_bp = Blueprint('bmi', __name__)

@bmi_bp.route('/', methods=['POST'])
@token_required
def calculate_user_bmi(current_user):
    data = request.get_json()
    result, err = BMIService.process_bmi(data.get('weight'), data.get('height'))
    if err:
        return jsonify({"error": err}), 400
    return jsonify(result), 200
