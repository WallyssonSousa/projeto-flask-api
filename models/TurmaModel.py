dados_turmas = {"turmas": []}
id_turma = 1

def turmas_get():
    return dados_turmas["turmas"]

def turma_get_id(turma_id):
    return next((t for t in dados_turmas["turmas"] if t["id"] == turma_id), None)

def turma_post(nova_turma):
    global id_turma
    nova_turma["id"] = id_turma
    nova_turma["ativo"] = True
    dados_turmas["turmas"].append(nova_turma)
    id_turma += 1
    return nova_turma

def turma_PUT(turma_id, dados_atualizados):
    turma = turma_get_id(turma_id)
    if turma:
        turma.update(dados_atualizados)
    return turma

def turma_DELETE(turma_id):
    turma = turma_get_id(turma_id)
    if turma:
        dados_turmas["turmas"].remove(turma)
        return True
    return False