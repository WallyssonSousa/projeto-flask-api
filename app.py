from flask import Flask
from flask_jwt_extended import JWTManager
from config import configure_app
from database import db
from routes.AlunoRoute import aluno_bp
from routes.ProfessorRoute import professor_bp
from routes.TurmaRoute import turma_bp
from routes.AuthRoute import auth_bp
from routes.ApiRoute import api_bp
from swagger.swagger_config import configure_swagger

app = Flask(__name__)
configure_app(app)

jwt = JWTManager(app)
db.init_app(app)

configure_swagger(app)

with app.app_context():
    db.create_all()


app.register_blueprint(auth_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(turma_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"]
    )
