dados = {
    "professores":[],
    "turmas":[],
    "alunos":[]
}

def professores_get():
    return dados['professores']

def professores_get_id(professor_id):
    lista_professores = dados['professores']
    for dici in lista_professores:
        if dici['id'] == professor_id:
            return dici

def professores_post(dict):
    dados['professores'].append(dict)