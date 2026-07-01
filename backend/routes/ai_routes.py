import sys
import os
from flask import Blueprint, request, jsonify
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.auth_utils import token_required
from backend.services.ai_service import AIService

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/voice_consult', methods=['POST'])
def voice_consult():
    data = request.get_json()
    if not data or 'transcript' not in data:
        return jsonify({"error": "Transcript is required"}), 400

    try:
        result = AIService.process_voice_consult(data['transcript'])
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/analyze_food', methods=['POST'])
def analyze_food():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Image is required"}), 400

    try:
        result = AIService.analyze_food_image(data['image'], data.get('portion_size', ''))
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/analyze_face', methods=['POST'])
def analyze_face():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Image is required"}), 400

    try:
        result = AIService.analyze_face_image(data['image'])
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/analyze_blood_report', methods=['POST'])
def analyze_blood_report():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Image is required"}), 400

    try:
        result = AIService.analyze_blood_report(data['image'])
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/find_doctors', methods=['POST'])
def find_doctors():
    data = request.get_json()
    city = data.get('city')
    locality = data.get('locality')
    specialist = data.get('specialist')
    
    if not city or not locality or not specialist:
        return jsonify({"error": "City, locality, and specialist are required"}), 400

    try:
        result = AIService.find_doctors(city, locality, specialist)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/', methods=['POST'])
@token_required
def analyze_concerns(current_user):
    data = request.get_json()
    result = AIService.process_concerns(data.get('concerns'))
    return jsonify(result), 200
