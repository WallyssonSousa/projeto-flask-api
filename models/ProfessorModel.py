from utils.FucoesValidacao import calcular_idade, validar_data

dados_professores = {"professores": []}
id_professor = 1

def get_todos_professores():
    return dados_professores["professores"]

def get_professor_por_id(professor_id):
    return next((p for p in dados_professores["professores"] if p["id"] == professor_id), None)

def adicionar_professor(professor):
    global id_professor
    professor["id"] = id_professor
    professor["idade"] = calcular_idade(professor["data_nascimento"])
    dados_professores["professores"].append(professor)
    id_professor += 1
    return professor

def atualizar_professor(professor_id, novos_dados):
    professor = get_professor_por_id(professor_id)
    if not professor:
        return None

    if "data_nascimento" in novos_dados and validar_data(novos_dados["data_nascimento"]):
        professor["data_nascimento"] = novos_dados["data_nascimento"]
        professor["idade"] = calcular_idade(novos_dados["data_nascimento"])

    for chave in novos_dados:
        if chave not in ["id", "idade", "data_nascimento"]:
            professor[chave] = novos_dados[chave]
    return professor

def deletar_professor(professor_id):
    professor = get_professor_por_id(professor_id)
    if professor:
        dados_professores["professores"].remove(professor)
        return True
    return False