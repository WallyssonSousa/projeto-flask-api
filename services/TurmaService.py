from models.TurmaModel import Turma
from models.ProfessorModel import Professor
from database import db

def get_todas_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def get_turma_por_id(turma_id):
    turma = Turma.query.get(turma_id)
    return turma.to_dict() if turma else None

def adicionar_turma(dados):
    professor = Professor.query.get(dados["professor_id"])
    if not professor:
        return {"erro": "Professor com ID fornecido não encontrado"}, 404

    nova_turma = Turma(
        nome=dados["nome"],
        turno=dados["turno"],
        ativo=True,
        professor_id=professor.id
    )

    db.session.add(nova_turma)
    db.session.commit()

    return nova_turma.to_dict(), 201

def atualizar_turma(turma_id, dados):
    turma = Turma.query.get(turma_id)
    if not turma:
        return {"erro": "Turma não encontrada"}, 404

    if "nome" in dados:
        turma.nome = dados["nome"]

    if "turno" in dados:
        turma.turno = dados["turno"]

    if "ativo" in dados:
        turma.ativo = dados["ativo"]

    if "professor_id" in dados:
        professor = Professor.query.get(dados["professor_id"])
        if not professor:
            return {"erro": "Professor com ID fornecido não encontrado"}, 404
        turma.professor_id = professor.id

    db.session.commit()
    return turma.to_dict(), 200

def deletar_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return {"erro": "Turma não encontrada"}, 404

    db.session.delete(turma)
    db.session.commit()
    return {"mensagem": "Turma removida"}, 200
