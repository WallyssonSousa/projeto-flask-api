# Simulação do "banco"
dados_professores = {"professores": []}
id_professor = 1

def get_todos_professores():
    return dados_professores["professores"]

def get_professor_por_id(prof_id):
    return next((p for p in dados_professores["professores"] if p["id"] == prof_id), None)

def adicionar_professor(professor):
    global id_professor
    professor["id"] = id_professor
    dados_professores["professores"].append(professor)
    id_professor += 1
    return professor

def atualizar_professor(prof_id, dados):
    professor = get_professor_por_id(prof_id)
    if professor:
        professor.update(dados)
    return professor

def deletar_professor(prof_id):
    professor = get_professor_por_id(prof_id)
    if professor:
        dados_professores["professores"].remove(professor)
        return True
    return False