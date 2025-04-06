from flask import Flask, jsonify, request
import sys
import os
sys.path.append(os.path.abspath('../PROJETO-FLASK-API'))
from app import validar_campos_obrigatorios



dados = {
    "professores":[],
    "turmas":[],
    "alunos":[]
}

def turmas_get():
    return jsonify(dados['turmas'])



def turma_get_id(turma_id):
    turma = None
    for t in dados['turmas']: # Percorre a lista de turmas no dicionario 'dados'
        if t["id"] == turma_id: # Verifica se o 'id' da turma é igual ao 'turma_id' fornecido
            turma = t
            break  # Sai do loop quando encontrar
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404
    
    # busca os dados do professor da turma
    professor = None
    for p in dados["professores"]: # Percorre a lista de professores no dicionario 'dados'
        if p['id'] == turma['professor_id']: # verifica se o 'id' do professor é igual ao 'id' de professor que está na turma com o 'id' informado
            professor = p # acha o professor da turma
            break # sai do loop quando achar
    if professor:
        novo_dici_professor = {} # Cria um novo dicionário para armazenar os valores do professor sem a chave 'turmas'
        for key, value in professor.items():         # Itera sobre cada chave e valor no dicionário original
            if key != 'turmas':             # Adiciona ao novo dicionário apenas as chaves diferentes de 'turmas'
                novo_dici_professor[key] = value
        
        professor = novo_dici_professor        # Atualiza o dicionário professor com o novo dicionário
        turma["professor"] = professor  # Inclui o professor na resposta    
    return jsonify(turma)



def turma_post():
    global id_turma  

    nova_turma = request.get_json()
    if not nova_turma:
        return jsonify({"error": "Nenhum dado foi inserido"}), 400

    campos_obrigatorios = {'descricao', 'materia', 'turno', 'professor_id'}
    erro, status = validar_campos_obrigatorios(nova_turma, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    if not any(p["id"] == nova_turma["professor_id"] for p in dados['professores']):
        return jsonify({"error": "Professor com ID fornecido não encontrado"}), 404

    nova_turma_formatada = {
        "id": id_turma,
        "descricao": nova_turma["descricao"],
        "materia": nova_turma["materia"],
        "turno": nova_turma["turno"],
        "professor_id": nova_turma["professor_id"],
        "ativo": True  
    }

    dados['turmas'].append(nova_turma_formatada)
    id_turma += 1  

    return jsonify({"mensagem": "Nova turma adicionada!", "turma": nova_turma_formatada}), 201



def turma_PUT(turma_id):
    atualizacoes = request.get_json()
    campos_permitidos = {'descricao', 'professor_id', 'ativo'}

    turma = None
    for t in dados['turmas']:
        if t['id'] == turma_id:
            turma = t
            break
    if not turma:
        return jsonify({"error": "Turma não encontrada!"}), 404

    campos_invalidos = []
    for chave in atualizacoes.keys():         
        if chave not in campos_permitidos: # Verifica se a chave não está na lista de campos permitidos
            campos_invalidos.append(chave)             # Adiciona a chave à lista de campos inválidos


    if campos_invalidos:
        return jsonify({"erro": "Campos inválidos", "campos_invalidos": campos_invalidos}), 400

    for chave, valor in atualizacoes.items():   # Percorre os itens que foram enviados para atualizar
        if chave in campos_permitidos:     # Verifica se a chave está na lista de campos permitidos
            turma[chave] = valor        # Atualiza o valor correspondente as chaves de turma

    return jsonify(turma), 200



def turma_DELETE(turma_id):
    turma = None
    for t in dados['turmas']:
        if t['id'] == turma_id:
            turma = t
            break
    if turma:
        dados['turmas'].remove(turma)
        return jsonify({"mensagem": "Turma removida"}), 200
    return jsonify({"error": "Turma não encontrada!"}), 404