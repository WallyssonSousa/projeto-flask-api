from flask import Blueprint, request, jsonify
from models.ProfessorModel import (
    get_todos_professores,
    get_professor_por_id,
    adicionar_professor,
    atualizar_professor,
    deletar_professor
)
from utils.FucoesValidacao import validar_data, calcular_idade, validar_campos_obrigatorios
from flask_jwt_extended import jwt_required, get_jwt

professor_bp = Blueprint('professores', __name__)

@professor_bp.route('/professores', methods=['GET'])
@jwt_required()
def get_professores():
    try:
        professores = get_todos_professores()
        return jsonify(professores), 200
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao listar professores: {str(e)}"}), 500

@professor_bp.route('/professores/<int:prof_id>', methods=['GET'])
@jwt_required()
def get_professor_by_id(prof_id):
    try:
        professor = get_professor_por_id(prof_id)
        if not professor:
            return jsonify({"erro": "Professor não encontrado"}), 404
        return jsonify(professor), 200
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao buscar o professor: {str(e)}"}), 500

@professor_bp.route('/professores', methods=['POST'])
@jwt_required()
def create_professor():
        
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem criar professores"}), 403
    
    dados = request.json
    campos_obrigatorios = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}
    erro, status = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if erro:
        return jsonify(erro), status
    if not validar_data(dados["data_nascimento"]):
        return jsonify({"erro": "Formato de data inválido, use YYYY-MM-DD"}), 400
    
    try:
        dados["idade"] = calcular_idade(dados["data_nascimento"])
        novo_professor = adicionar_professor(dados)
        return jsonify(novo_professor), 201
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao criar um professor: {str(e)}"}), 500

@professor_bp.route('/professores/<int:prof_id>', methods=['PUT'])
@jwt_required()
def update_professor(prof_id):
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem atualizar professores"}), 403

    dados = request.json
    campos_permitidos = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}

    campos_invalidos = [chave for chave in dados.keys() if chave not in campos_permitidos]
    if "id" in dados or "idade" in dados:
        return jsonify({"erro": "O ID e a idade não podem ser alterados"}), 400
    if campos_invalidos:
        return jsonify({"erro": "Campos inválidos", "campos_invalidos": campos_invalidos}), 400

    professor = get_professor_por_id(prof_id)
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404
    if "data_nascimento" in dados:
        if not validar_data(dados["data_nascimento"]):
            return jsonify({"erro": "Formato de data inválido, use YYYY-MM-DD"}), 400
        dados["idade"] = calcular_idade(dados["data_nascimento"])
    try:
        professor_atualizado = atualizar_professor(prof_id, dados)
        return jsonify(professor_atualizado), 200
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao atualizar o professor: {str(e)}"}), 500

@professor_bp.route('/professores/<int:prof_id>', methods=['DELETE'])
@jwt_required()
def delete_professor(prof_id):
    jwt_claims = get_jwt()
    if jwt_claims.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem excluir professores"}), 403

    try:
        if deletar_professor(prof_id):
            return jsonify({"mensagem": "Professor removido"}), 200
        return jsonify({"erro": "Professor não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao excluir o professor: {str(e)}"}), 500