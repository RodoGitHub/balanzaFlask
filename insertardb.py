from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Persona
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def insertar_usuarios():
    with app.app_context():
        db.create_all()
        password_plano = '1234'  # Contraseña en texto plano
        password_hasheada = generate_password_hash(password_plano)  # Hashear la contraseña
        
        # Imprimir la contraseña hasheada
        print(f"Contraseña hasheada: {password_hasheada}")
        
        usuarios = [
            Usuario(
                nombre_usuario='admin3',
                password=password_hasheada,  # Usar la contraseña hasheada
                rol_id=1,
                persona_id=1
            ),
        ]

        print("Usuarios insertados correctamente.")

if __name__ == '__main__':
    insertar_usuarios()