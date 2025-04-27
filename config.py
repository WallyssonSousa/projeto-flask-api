from datetime import timedelta
import os
from dotenv import load_dotenv


def configure_app(app):
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['HOST'] = '0.0.0.0'
    app.config['PORT'] = 5000
    app.config['DEBUG'] = True
    print("Banco de dados:", app.config['SQLALCHEMY_DATABASE_URI'])

