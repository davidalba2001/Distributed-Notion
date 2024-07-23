#dependencias
from flask import Flask
from src.app.config import SECRET_KEY
from src.app.auth import auth

#inicializar la app
def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = SECRET_KEY
  app.register_blueprint(auth)
  return app

