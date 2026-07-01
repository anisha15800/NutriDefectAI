import sys
import os
from flask import Blueprint, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from backend.services.assessment_service import AssessmentService

assessment_bp = Blueprint('assessment', __name__)

@assessment_bp.route('/suggest_symptoms', methods=['POST'])
def suggest_symptoms():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Please provide current symptoms"}), 400

    try:
        suggestions = AssessmentService.suggest_symptoms(data['symptoms'])
        return jsonify({"suggestions": suggestions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@assessment_bp.route('/final', methods=['POST'])
# Using optional token if we want guest access, but let's assume token_required is okay if user is logged in
# Actually, since nutrition_check is accessible by logged in users, we'll try to extract email if token exists, 
# but we won't strictly enforce it here to avoid breaking if they are testing without login.
def final_assessment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Optional auth extraction (simplification)
    user_email = data.get('email', None) 

    try:
        result = AssessmentService.generate_final_report(data, user_email)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@assessment_bp.route('/followup', methods=['POST'])
def generate_followup():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Symptoms are required"}), 400

    try:
        questions = AssessmentService.generate_followup_questions(data)
        return jsonify({"questions": questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@assessment_bp.route('/generate_diet_plan', methods=['POST'])
def generate_diet_plan():
    data = request.get_json()
    if not data or 'deficiency' not in data:
        return jsonify({"error": "Deficiency is required"}), 400

    try:
        html_plan = AssessmentService.generate_diet_plan(data['deficiency'], data.get('user_data', {}))
        return jsonify({"html": html_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
