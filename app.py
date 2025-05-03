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
from werkzeug.security import generate_password_hash
from models.UserModel import User
from database import db
import os

app = Flask(__name__)
configure_app(app)

jwt = JWTManager(app)
db.init_app(app)

configure_swagger(app)

with app.app_context():
    db.create_all()

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        print("Variáveis ADMIN_USERNAME e ADMIN_PASSWORD devem estar definidas para criação do 1º usuário root.")
        exit(1)

    if User.query.filter_by(username=admin_username).first():
        print(f"Usuário admin: '{admin_username}'")
    else:
        hashed_password = generate_password_hash(admin_password)
        admin = User(username=admin_username, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Usuário admin '{admin_username}' criado com sucesso.")


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
