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

def calcular_media_final(nota1, nota2):
    try:
        # Garante que as notas são convertidas para float
        nota1 = float(nota1)
        nota2 = float(nota2)

        # Verifica se as notas estão no intervalo válido (0 a 10, por exemplo)
        if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10):
            raise ValueError("Notas devem estar entre 0 e 10.")

        media = (nota1 + nota2) / 2
        return round(media, 2)  # Arredonda para 2 casas decimais

    except (ValueError, TypeError) as e:
        raise ValueError(f"Erro ao calcular média: {e}")
