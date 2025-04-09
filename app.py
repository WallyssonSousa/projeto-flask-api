import os
from config import app
from routes.AlunoRoute import aluno_bp
from routes.ProfessorRoute import professor_bp
from routes.TurmaRoute import turma_bp

app.register_blueprint(aluno_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(turma_bp)

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )