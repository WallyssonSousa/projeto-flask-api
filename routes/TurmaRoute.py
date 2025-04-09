from flask import Blueprint
from models.TurmaModel import turmas_get, turma_get_id, turma_post, turma_PUT, turma_DELETE

turma_bp = Blueprint('turma_bp', __name__)

# Rota para listar todas as turmas
@turma_bp.route('/turmas', methods=['GET'])
def listar_turmas():
    return turmas_get()

# Rota para obter uma turma específica pelo ID
@turma_bp.route('/turmas/<int:turma_id>', methods=['GET'])
def obter_turma(turma_id):
    return turma_get_id(turma_id)

# Rota para adicionar uma nova turma
@turma_bp.route('/turmas', methods=['POST'])
def criar_turma():
    return turma_post()

# Rota para atualizar uma turma existente
@turma_bp.route('/turmas/<int:turma_id>', methods=['PUT'])
def atualizar_turma(turma_id):
    return turma_PUT(turma_id)

# Rota para deletar uma turma
@turma_bp.route('/turmas/<int:turma_id>', methods=['DELETE'])
def deletar_turma(turma_id):
    return turma_DELETE(turma_id)