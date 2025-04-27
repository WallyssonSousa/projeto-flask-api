from database import db

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)

    alunos = db.relationship('Aluno', back_populates='turma', cascade='all, delete-orphan')
    professor = db.relationship('Professor', back_populates='turmas')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "turno": self.turno,
            "ativo": self.ativo,
            "professor_id": self.professor_id,
            "professor": self.professor.to_dict() if self.professor else None
        }
