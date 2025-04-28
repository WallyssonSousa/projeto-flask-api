from flask import Blueprint, jsonify, request


api_bp = Blueprint("api_bp", __name__)

@api_bp.route('/', methods=['GET'])
def api_root():
    return jsonify({"message": "API is running"}), 200
