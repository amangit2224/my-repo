from flask import Blueprint, request, jsonify, current_app
from utils.ai_explainer import explain_medical_term

jargon_bp = Blueprint('jargon', __name__)

@jargon_bp.route('/explain', methods=['POST'])
def explain():
    data = request.get_json()
    term = data.get('term', '').strip()

    if not term:
        return jsonify({"error": "Term is required"}), 400

    try:
        result = explain_medical_term(term)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500