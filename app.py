import os
from dotenv import load_dotenv
from config import app
from routes.AlunoRoute import aluno_bp
from routes.ProfessorRoute import professor_bp
from routes.TurmaRoute import turma_bp
from routes.AuthRoute import auth_bp
from flask_jwt_extended import JWTManager

load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(aluno_bp, url_prefix='/aluno')
app.register_blueprint(professor_bp, url_prefix='/professor')
app.register_blueprint(turma_bp, url_prefix='/turma')

if __name__ == '__main__':
    app.run(
        host=app.config["HOST"],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
