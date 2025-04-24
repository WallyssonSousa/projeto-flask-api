from flask import Blueprint, request, jsonify
from models.TurmaModel import turmas_get, turma_get_id, turma_post, turma_PUT, turma_DELETE
from flask_jwt_extended import jwt_required, get_jwt
from utils.FucoesValidacao import validar_campos_obrigatorios, validar_campos_obrigatorios
from models.ProfessorModel import dados_professores

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
    campos_obrigatorios = ["nome", "turno", "professor_id"]
    erro, status = validar_campos_obrigatorios(nova_turma, campos_obrigatorios)
    if erro:
        return jsonify({"erro": erro}), status
    if not any(p["id"] == nova_turma["professor_id"] for p in dados_professores["professores"]):
        return jsonify({"erro": "Professor com o ID fornecido não encontrado"}), 404
    
    try:
        turma_criada = turma_post(nova_turma)
        return jsonify(turma_criada), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao ao criar turma: {str(e)}"}), 500
    
# Rota para atualizar uma turma existente
@turma_bp.route('/turmas/<int:turma_id>', methods=['PUT'])
@jwt_required()
def update_turma(turma_id):
    user = get_jwt()
    if user.get("role") != "admin":
        return jsonify({"erro": "Acesso negado: apenas administradores podem atualizar turmas existentes"}), 403
    
    dados_atualizados = request.get_json()
    if not dados_atualizados:
        return jsonify({"erro": "Dados ausentes ou inválidos"}), 400
    
    campos_permitidos = {"nome", "professor_id", "ativo"}
    campos_invalidos = [campo for campo in dados_atualizados if campo not in campos_permitidos]
    if campos_invalidos:
        return jsonify({
            "erro": "Campos inválidos enviados para atualização",
            "campos_invalidos": campos_invalidos
        }), 400
    if "professor_id" in dados_atualizados:
        if not any(p["id"] == dados_atualizados["professor_id"] for p in dados_professores["professores"]):
            return jsonify({"erro": "Professor com ID fornecido não encontrado"}), 404
    try:
        turma = turma_PUT(turma_id, dados_atualizados)
        if turma:
            return jsonify(turma), 200
        return jsonify({"erro": "Turma não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro ao atulizar a turma: {str(e)}"}), 500

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
        return jsonify({"erro": f"Erro ao tentar deletar turma: {str(e)}"}), 500