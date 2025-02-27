import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Importa db desde models.py
from models import db

# Cargar variables de entorno antes de utilizarlas
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Conecta db a la app
db.init_app(app)
CORS(app, origins=["http://localhost:5173"])
migrate = Migrate(app, db)
jwt = JWTManager(app)
ma = Marshmallow(app)

# Importa tus modelos después de inicializar db y migrate
from models import *

from views import register_bp
register_bp(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)