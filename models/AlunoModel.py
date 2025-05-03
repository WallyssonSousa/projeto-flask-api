from database import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)

    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    turma = db.relationship('Turma', back_populates='alunos')

    def to_dict(self): 
        return {
            "id": self.id, 
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.strftime("%Y-%m-%d"),
            "idade": self.idade,
            "nota_primeiro_semestre": self.nota_primeiro_semestre,
            "nota_segundo_semestre": self.nota_segundo_semestre,
            "media_final": self.media_final,
            "turma_id": self.turma_id,
            "turma": self.turma.to_dict() if self.turma else None
        }

def get_todos_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]
