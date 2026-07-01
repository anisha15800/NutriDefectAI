from flask import Blueprint, request, jsonify
from services.prediction_service import PredictionService

prediction_bp = Blueprint('prediction', __name__)
prediction_service = PredictionService()

@prediction_bp.route('/', methods=['POST'])
def predict_deficiency():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Please provide symptoms data"}), 400

    try:
        result = prediction_service.predict(data['symptoms'])
        return jsonify({
            "message": "Prediction successful",
            "data": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
