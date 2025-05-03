from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.UserModel import User
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import os

from utils.VerificacaoTypeAdmin import is_admin_user

auth_bp = Blueprint('auth', __name__)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    if not is_admin_user():
        return jsonify({"erro": "Apenas administradores podem visualizar os usuários."}), 403
    
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify({"users": user_list}), 200

@auth_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not is_admin_user():
        return jsonify({"erro": "Apenas administradores podem deletar usuários."}), 403

    user_to_delete = User.query.get(user_id)

    if not user_to_delete:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    if user_to_delete.username == ADMIN_USERNAME:
        return jsonify({"erro": "Não é permitido excluir administradores raiz"}), 403

    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({"message": "Usuário deletado com sucesso."}), 200

                                    
@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"erro": "Preencha username e password"}), 400

    if "admin" in username.lower() or "admin" in password.lower():
        return jsonify({"erro": "Nome de usuário ou senha não podem conter a palavra 'admin'"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"erro": "Usuário já existe"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"erro": "Dados de login incompletos"}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        role = "admin" if username == ADMIN_USERNAME else "usuario"

        access_token = create_access_token(
            identity=username,
            additional_claims={"role": role}
        )

    
        user.token = access_token
        db.session.commit()

        return jsonify({"access_token": access_token}), 200

    return jsonify({"erro": "Credenciais inválidas"}), 401


@auth_bp.route('/create_admin', methods=['POST'])
@jwt_required()  
def create_admin():
    current_user = get_jwt_identity()
    current_user_role = get_jwt().get('role', None)

    if current_user_role != 'admin':
        return jsonify({"erro": "Apenas administradores raiz podem criar novos admins"}), 403

    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"erro": "Preencha username e password"}), 400

    # Admins podem criar usuários com 'admin' no nome
    if User.query.filter_by(username=username).first():
        return jsonify({"erro": "Usuário já existe"}), 400

    hashed_password = generate_password_hash(password)
    new_admin = User(username=username, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": f"Usuário '{username}' criado com sucesso"}), 201



@auth_bp.route('/protected', methods=['GET'])
@jwt_required() 
def protected():
    current_user = get_jwt_identity()  
    return jsonify(logged_in_as=current_user), 200
