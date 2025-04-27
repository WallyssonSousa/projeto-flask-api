from models.ProfessorModel import Professor
from database import db
from utils.FucoesValidacao import calcular_idade, validar_data

def get_todos_professores():
    professores = Professor.query.all()
    return [prof.to_dict() for prof in professores]

def get_professor_por_id(professor_id):
    professor = Professor.query.get(professor_id)
    return professor.to_dict() if professor else None

def adicionar_professor(dados):
    if not validar_data(dados["data_nascimento"]):
        return {"erro": "Data de nascimento inválida"}, 400

    novo_professor = Professor(
        nome=dados["nome"],
        data_nascimento=dados["data_nascimento"],
        idade=calcular_idade(dados["data_nascimento"]),
        disciplina=dados["disciplina"],
        salario=dados["salario"],
        observacoes=dados.get("observacoes", "")
    )

    db.session.add(novo_professor)
    db.session.commit()
    return novo_professor.to_dict(), 201

def atualizar_professor(professor_id, dados):
    professor = Professor.query.get(professor_id)
    if not professor:
        return {"erro": "Professor não encontrado"}, 404

    if "nome" in dados:
        professor.nome = dados["nome"]

    if "data_nascimento" in dados:
        if not validar_data(dados["data_nascimento"]):
            return {"erro": "Data de nascimento inválida"}, 400
        professor.data_nascimento = dados["data_nascimento"]
        professor.idade = calcular_idade(dados["data_nascimento"])

    if "disciplina" in dados:
        professor.disciplina = dados["disciplina"]

    if "salario" in dados:
        professor.salario = dados["salario"]

    if "observacoes" in dados:
        professor.observacoes = dados["observacoes"]

    db.session.commit()
    return professor.to_dict(), 200

def deletar_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return {"erro": "Professor não encontrado"}, 404

    db.session.delete(professor)
    db.session.commit()
    return {"mensagem": "Professor removido"}, 200
