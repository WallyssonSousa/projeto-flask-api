from flask import Blueprint, request, jsonify
from services.ProfessorService import (
    get_todos_professores,
    get_professor_por_id,
    adicionar_professor,
    atualizar_professor,
    deletar_professor
)
from flask_jwt_extended import jwt_required, get_jwt
from utils.FucoesValidacao import validar_campos_obrigatorios

professor_bp = Blueprint('professor_bp', __name__)

@professor_bp.route('/professores', methods=['GET'])
@jwt_required()
def listar_professores():
    try:
        return jsonify(get_todos_professores()), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar professores: {str(e)}"}), 500

@professor_bp.route('/professores/<int:professor_id>', methods=['GET'])
@jwt_required()
def obter_professor(professor_id):
    try:
        professor = get_professor_por_id(professor_id)
        if professor:
            return jsonify(professor), 200
        return jsonify({"erro": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao obter professor: {str(e)}"}), 500

@professor_bp.route('/professores', methods=['POST'])
@jwt_required()
def criar_professor():
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Apenas administradores podem criar professores"}), 403

    dados = request.get_json()
    campos_obrigatorios = ["nome", "data_nascimento", "disciplina", "salario", "observacoes"]
    erro, status = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    try:
        professor, status = adicionar_professor(dados)
        return jsonify(professor), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar professor: {str(e)}"}), 500

@professor_bp.route('/professores/<int:professor_id>', methods=['PUT'])
@jwt_required()
def atualizar_professor_route(professor_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Apenas administradores podem atualizar professores"}), 403

    dados = request.get_json()
    campos_permitidos = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}
    campos_invalidos = [campo for campo in dados if campo not in campos_permitidos]
    if campos_invalidos:
        return jsonify({
            "erro": "Campos inválidos enviados",
            "campos_invalidos": campos_invalidos
        }), 400

    try:
        professor, status = atualizar_professor(professor_id, dados)
        return jsonify(professor), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar professor: {str(e)}"}), 500

@professor_bp.route('/professores/<int:professor_id>', methods=['DELETE'])
@jwt_required()
def deletar_professor_route(professor_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Apenas administradores podem excluir professores"}), 403

    try:
        resposta, status = deletar_professor(professor_id)
        return jsonify(resposta), status
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar professor: {str(e)}"}), 500
