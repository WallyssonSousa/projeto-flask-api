from utils import calcular_idade, calcular_media_final, validar_data

dados_alunos = {"alunos": []}
id_aluno = 1

def get_todos_alunos():
    return dados_alunos["alunos"]

def get_aluno_por_id(aluno_id):
    return next((a for a in dados_alunos["alunos"] if a["id"] == aluno_id), None)

def adicionar_aluno(dados, dados_turmas):
    global id_aluno

    if not validar_data(dados["data_nascimento"]):
        return {"erro": "Formato de data inválido, use YYYY-MM-DD"}, 400

    if not any(t["id"] == dados["turma_id"] for t in dados_turmas["turmas"]):
        return {"erro": "Turma com ID fornecido não encontrada"}, 404

    dados["idade"] = calcular_idade(dados["data_nascimento"])
    dados["media_final"] = calcular_media_final(dados["nota_primeiro_semestre"], dados["nota_segundo_semestre"])
    dados["id"] = id_aluno
    dados_alunos["alunos"].append(dados)
    id_aluno += 1
    return dados, 201

def atualizar_aluno(aluno_id, dados, dados_turmas):
    aluno = get_aluno_por_id(aluno_id)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404

    if "id" in dados or "idade" in dados:
        return {"erro": "O ID e a idade do aluno não podem ser alterados"}, 400

    if not any(t["id"] == dados["turma_id"] for t in dados_turmas["turmas"]):
        return {"erro": "Turma com ID fornecido não encontrada"}, 404

    if "data_nascimento" in dados and not validar_data(dados["data_nascimento"]):
        return {"erro": "Formato de data inválido, use YYYY-MM-DD"}, 400

    if "data_nascimento" in dados:
        dados["idade"] = calcular_idade(dados["data_nascimento"])
    if "nota_primeiro_semestre" in dados and "nota_segundo_semestre" in dados:
        dados["media_final"] = calcular_media_final(dados["nota_primeiro_semestre"], dados["nota_segundo_semestre"])

    for chave, valor in dados.items():
        aluno[chave] = valor

    return aluno, 200

def deletar_aluno(aluno_id):
    aluno = get_aluno_por_id(aluno_id)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404
    dados_alunos["alunos"].remove(aluno)
    return {"mensagem": "Aluno removido"}, 200