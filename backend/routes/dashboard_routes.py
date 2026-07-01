import sys
import os
from flask import Blueprint, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@token_required
def get_dashboard_summary(current_user):
    # Mock dashboard summary data
    return jsonify({
        "status": "success",
        "summary": "Dashboard data fetched successfully."
    }), 200
