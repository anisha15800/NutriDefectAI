import sys
import os
from flask import Blueprint, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from services.consult_service import ConsultService

consult_bp = Blueprint('consult', __name__)

@consult_bp.route('/doctors', methods=['GET'])
@token_required
def list_doctors(current_user):
    return jsonify(ConsultService.get_available_doctors()), 200

@consult_bp.route('/book', methods=['POST'])
@token_required
def book_consultation(current_user):
    data = request.get_json()
    doctor_id = data.get("doctor_id")
    result = ConsultService.book_consult(doctor_id, current_user.get('sub'))
    return jsonify(result), 200
