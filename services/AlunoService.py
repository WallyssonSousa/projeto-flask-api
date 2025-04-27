from models.AlunoModel import Aluno
from models.TurmaModel import Turma
from database import db
from datetime import datetime
from utils.FucoesValidacao import validar_data, calcular_idade, calcular_media_final

def get_todos_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def get_aluno_por_id(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    return aluno.to_dict() if aluno else None

def adicionar_aluno(dados):
    if not validar_data(dados["data_nascimento"]):
        return {"erro": "Formato de data inválido, use YYYY-MM-DD"}, 400

    turma = Turma.query.get(dados["turma_id"])
    if not turma:
        return {"erro": "Turma com ID fornecido não encontrada"}, 404

    novo_aluno = Aluno(
        nome=dados["nome"],
        data_nascimento=datetime.strptime(dados["data_nascimento"], '%Y-%m-%d').date(),
        idade=calcular_idade(dados["data_nascimento"]),
        nota_primeiro_semestre=dados["nota_primeiro_semestre"],
        nota_segundo_semestre=dados["nota_segundo_semestre"],
        media_final=calcular_media_final(dados["nota_primeiro_semestre"], dados["nota_segundo_semestre"]),
        turma_id=turma.id
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return novo_aluno.to_dict(), 201


def atualizar_aluno(aluno_id, dados):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404

    if "id" in dados or "idade" in dados:
        return {"erro": "O ID e a idade do aluno não podem ser alterados"}, 400

    if "turma_id" in dados:
        turma = Turma.query.get(dados["turma_id"])
        if not turma:
            return {"erro": "Turma com ID fornecido não encontrada"}, 404
        aluno.turma_id = turma.id

    if "data_nascimento" in dados:
        if not validar_data(dados["data_nascimento"]):
            return {"erro": "Formato de data inválido, use YYYY-MM-DD"}, 400
        aluno.data_nascimento = datetime.strptime(dados["data_nascimento"], '%Y-%m-%d').date()
        aluno.idade = calcular_idade(dados["data_nascimento"])

    if "nota_primeiro_semestre" in dados:
        aluno.nota_primeiro_semestre = dados["nota_primeiro_semestre"]

    if "nota_segundo_semestre" in dados:
        aluno.nota_segundo_semestre = dados["nota_segundo_semestre"]

    if "nota_primeiro_semestre" in dados or "nota_segundo_semestre" in dados:
        aluno.media_final = calcular_media_final(aluno.nota_primeiro_semestre, aluno.nota_segundo_semestre)

    if "nome" in dados:
        aluno.nome = dados["nome"]

    db.session.commit()

    return aluno.to_dict(), 200

def deletar_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return {"erro": "Aluno não encontrado"}, 404

    db.session.delete(aluno)
    db.session.commit()

    return {"mensagem": "Aluno removido"}, 200
