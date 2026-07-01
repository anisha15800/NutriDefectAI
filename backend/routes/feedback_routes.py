import sys
import os
from flask import Blueprint, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from services.feedback_service import FeedbackService

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/', methods=['POST'])
@token_required
def submit_feedback(current_user):
    data = request.get_json()
    result = FeedbackService.submit_feedback(current_user.get('sub'), data.get('message'))
    return jsonify(result), 200
