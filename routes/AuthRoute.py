from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'senha123'

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"erro": "Dados de login incompletos"}), 400

    username = data['username']
    password = data['password']

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
   
        access_token = create_access_token(
            identity=username, 
            additional_claims={"role": "admin"}  
        )
        return jsonify(access_token=access_token), 200

    if username == 'usuario' and password == 'senha123':
        access_token = create_access_token(
            identity=username,  
            additional_claims={"role": "usuario"} 
        )
        return jsonify(access_token=access_token), 200

    return jsonify({"erro": "Credenciais inválidas"}), 401
