from database import db

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text)

    turmas = db.relationship('Turma', back_populates='professor', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.strftime('%Y-%m-%d'),
            "idade": self.idade,
            "disciplina": self.disciplina,
            "salario": self.salario,
            "observacoes": self.observacoes
        }
