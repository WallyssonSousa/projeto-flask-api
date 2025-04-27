from flask import Blueprint, request, jsonify
from services.TurmaService import (
    get_todas_turmas, get_turma_por_id, adicionar_turma, 
    atualizar_turma, deletar_turma
)
from flask_jwt_extended import jwt_required, get_jwt
from utils.FucoesValidacao import validar_campos_obrigatorios

turma_bp = Blueprint('turma_bp', __name__)

@turma_bp.route('/turmas', methods=['GET'])
@jwt_required()
def listar_turmas():
    try:
        return jsonify(get_todas_turmas()), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar turmas: {str(e)}"}), 500

@turma_bp.route('/turmas/<int:turma_id>', methods=['GET'])
@jwt_required()
def obter_turma(turma_id):
    try:
        turma = get_turma_por_id(turma_id)
        if turma:
            return jsonify(turma), 200
        return jsonify({"erro": "Turma não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao obter turma: {str(e)}"}), 500

@turma_bp.route('/turmas', methods=['POST'])
@jwt_required()
def criar_turma():
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Apenas administradores podem criar turmas"}), 403

    dados = request.get_json()
    campos_obrigatorios = ["nome", "turno", "professor_id"]
    erro, status = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    try:
        turma, status = adicionar_turma(dados)
        return jsonify(turma), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar turma: {str(e)}"}), 500

@turma_bp.route('/turmas/<int:turma_id>', methods=['PUT'])
@jwt_required()
def atualizar_turma_route(turma_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Apenas administradores podem atualizar turmas"}), 403

    dados = request.get_json()
    campos_permitidos = {"nome", "turno", "ativo", "professor_id"}
    campos_invalidos = [campo for campo in dados if campo not in campos_permitidos]
    if campos_invalidos:
        return jsonify({
            "erro": "Campos inválidos enviados",
            "campos_invalidos": campos_invalidos
        }), 400

    try:
        turma, status = atualizar_turma(turma_id, dados)
        return jsonify(turma), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar turma: {str(e)}"}), 500

@turma_bp.route('/turmas/<int:turma_id>', methods=['DELETE'])
@jwt_required()
def deletar_turma_route(turma_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Apenas administradores podem excluir turmas"}), 403

    try:
        resposta, status = deletar_turma(turma_id)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar turma: {str(e)}"}), 500
