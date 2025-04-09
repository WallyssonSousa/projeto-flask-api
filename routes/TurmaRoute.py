from flask import Blueprint, request, jsonify
from models.TurmaModel import turmas_get, turma_get_id, turma_post, turma_PUT, turma_DELETE

turma_bp = Blueprint('turma_bp', __name__)

# Rota para listar todas as turmas
@turma_bp.route('/turmas', methods=['GET'])
def listar_turmas():
    return turmas_get()

# Rota para obter uma turma específica pelo ID
@turma_bp.route('/turmas/<int:turma_id>', methods=['GET'])
def obter_turma(turma_id):
    turma = turma_get_id(turma_id)
    if turma is None:
        return jsonify({"erro": "Turma não encontrada"}), 404
    return jsonify(turma), 200

# Rota para adicionar uma nova turma
@turma_bp.route('/turmas', methods=['POST'])
def criar_turma():
    nova_turma = request.get_json()
    turma = turma_post(nova_turma)
    return jsonify(turma), 201

# Rota para atualizar uma turma existente
@turma_bp.route('/turmas/<int:turma_id>', methods=['PUT'])
def atualizar_turma(turma_id):
    dados_atualizados = request.get_json()
    turma = turma_PUT(turma_id, dados_atualizados)
    if turma:
        return jsonify(turma), 200
    return jsonify({"erro": "Turma não encontrada"}), 404

# Rota para deletar uma turma
@turma_bp.route('/turmas/<int:turma_id>', methods=['DELETE'])
def deletar_turma(turma_id):
    resposta, status = turma_DELETE(turma_id)
    return jsonify(resposta), status