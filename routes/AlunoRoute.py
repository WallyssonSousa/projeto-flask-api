from flask import Blueprint, request, jsonify
from models.AlunoModel import (
    get_todos_alunos, get_aluno_por_id, adicionar_aluno,
    atualizar_aluno, deletar_aluno
)
from models.TurmaModel import dados_turmas
from utils.FucoesValidacao import validar_campos_obrigatorios

aluno_bp = Blueprint("aluno_bp", __name__)

@aluno_bp.route('/alunos', methods=['POST'])
def create_aluno():
    dados = request.json
    campos_obrigatorios = {"data_nascimento", "nome", "nota_primeiro_semestre", "nota_segundo_semestre", "turma_id"}

    erro, status = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    aluno, status = adicionar_aluno(dados, dados_turmas)
    return jsonify(aluno), status

@aluno_bp.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    dados = request.json
    campos_permitidos = {"data_nascimento", "nome", "nota_primeiro_semestre", "nota_segundo_semestre", "turma_id"}

    campos_invalidos = [k for k in dados.keys() if k not in campos_permitidos]
    if campos_invalidos:
        return jsonify({"erro": "Campos inválidos", "campos_invalidos": campos_invalidos}), 400

    aluno, status = atualizar_aluno(id, dados, dados_turmas)
    return jsonify(aluno), status

@aluno_bp.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(get_todos_alunos())

@aluno_bp.route('/alunos/<int:id>', methods=['GET'])
def get_aluno_by_id(id):
    aluno = get_aluno_por_id(id)
    if aluno:
        turma = next((t for t in dados_turmas["turmas"] if t["id"] == aluno["turma_id"]), None)
        if turma:
            aluno_completo = aluno.copy()
            aluno_completo["turma"] = turma
            return jsonify(aluno_completo)
        return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@aluno_bp.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    resultado, status = deletar_aluno(id)
    return jsonify(resultado), status