import sys
import os
from flask import Blueprint, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from services.nutrition_service import NutritionService

nutrition_bp = Blueprint('nutrition', __name__)

@nutrition_bp.route('/', methods=['POST'])
@token_required
def check_nutrition(current_user):
    data = request.get_json()
    result = NutritionService.process_nutrition_check(data)
    return jsonify(result), 200
