from datetime import datetime, date

def validar_data(data_str):
    try:
        datetime.strptime(data_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def calcular_idade(data_nascimento):
    nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
    hoje = date.today()
    return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

def validar_campos_obrigatorios(dados, campos_obrigatorios):
    faltando = [campo for campo in campos_obrigatorios if campo not in dados]
    if faltando:
        return {
            "erro": "Campos obrigatorios ausentes",
            "campos_faltando": faltando
        }, 400
    return None, 200