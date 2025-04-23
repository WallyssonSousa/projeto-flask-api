from flask import Blueprint, request, jsonify
from models.TurmaModel import turmas_get, turma_get_id, turma_post, turma_PUT, turma_DELETE
from flask_jwt_extended import jwt_required, get_jwt
from utils.FucoesValidacao import validar_campos_obrigatorios

turma_bp = Blueprint('turma_bp', __name__)

@turma_bp.route('/turmas', methods=['GET'])
@jwt_required()
def get_turmas():
    try:
        return jsonify(turmas_get()), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar turmas: {str(e)}"}), 500

@turma_bp.route('/turmas/<int:turma_id>', methods=['GET'])
@jwt_required()
def get_turma_by_id(turma_id):
    try:
        turma = turma_get_id(turma_id)
        if turma is None:
            return jsonify({"erro": "Turma não encontrada"}), 404
        return jsonify(turma), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao obter turma: {str(e)}"}), 500

@turma_bp.route('/turmas', methods=['POST'])
@jwt_required()
def create_turma():
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar novas turmas"}), 403

    nova_turma = request.json
    campos_obrigatorios = ["nome", "ano", "semestre", "curso_id"]

    erro, status = validar_campos_obrigatorios(nova_turma, campos_obrigatorios)
    if erro:
        return jsonify({"erro": erro}), status

# Rota para atualizar uma turma existente
@turma_bp.route('/turmas/<int:turma_id>', methods=['PUT'])
@jwt_required()
def update_turma(turma_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem atualizar turmas existentes"}), 403

    try:
        dados_atualizados = request.get_json()
        if not dados_atualizados:
            return jsonify({"erro": "Dados ausentes ou inválidos"}), 400

        turma = turma_PUT(turma_id, dados_atualizados)
        if turma:
            return jsonify(turma), 200
        return jsonify({"erro": "Turma não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar turma: {str(e)}"}), 500

# Rota para deletar uma turma
@turma_bp.route('/turmas/<int:turma_id>', methods=['DELETE'])
@jwt_required()
def delete_turma(turma_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem excluir turmas existentes"}), 403

    try:
        resposta, status = turma_DELETE(turma_id)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar turma: {str(e)}"}), 500