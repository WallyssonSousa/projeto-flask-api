from flask import Blueprint, request, jsonify
from models.ProfessorModel import (
    get_todos_professores,
    get_professor_por_id,
    adicionar_professor,
    atualizar_professor,
    deletar_professor
)
from utils.FucoesValidacao import validar_data, calcular_idade, validar_campos_obrigatorios

professor_bp = Blueprint('professores', __name__)

@professor_bp.route('', methods=['GET'])
def listar_professores():
    return jsonify(get_todos_professores())

@professor_bp.route('/<int:prof_id>', methods=['GET'])
def get_id_professor(prof_id):
    professor = get_professor_por_id(prof_id)
    if not professor:
        return jsonify({"erro": "Professor nao encontrado"}), 404
    return jsonify(professor)

@professor_bp.route('', methods=['POST'])
def post_professor():
    dados = request.json
    campos_obrigatorios = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}

    erro, status = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    if not validar_data(dados["data_nascimento"]):
        return jsonify({"erro": "Formato de data invalido, use YYYY-MM-DD"}), 400

    dados["idade"] = calcular_idade(dados["data_nascimento"])
    novo_professor = adicionar_professor(dados)

    return jsonify(novo_professor), 201

@professor_bp.route('/<int:prof_id>', methods=['PUT'])
def update_professor_route(prof_id):
    dados = request.json
    campos_permitidos = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}

    campos_invalidos = [chave for chave in dados.keys() if chave not in campos_permitidos]
    if "id" in dados or "idade" in dados:
        return jsonify({"erro": "O ID e a idade nao podem ser alterados"}), 400
    if campos_invalidos:
        return jsonify({"erro": "Campos invalidos", "campos_invalidos": campos_invalidos}), 400

    professor = get_professor_por_id(prof_id)
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    if "data_nascimento" in dados:
        if not validar_data(dados["data_nascimento"]):
            return jsonify({"erro": "Formato de data inválido, use YYYY-MM-DD"}), 400
        dados["idade"] = calcular_idade(dados["data_nascimento"])

    professor_atualizado = atualizar_professor(prof_id, dados)
    return jsonify(professor_atualizado)

@professor_bp.route('/<int:prof_id>', methods=['DELETE'])
def delete_professor_route(prof_id):
    if deletar_professor(prof_id):
        return jsonify({"mensagem": "Professor removido"}), 200
    return jsonify({"erro": "Professor nao encontrado"}), 404
