from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Persona  # Importamos db, Usuario y Persona desde models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializar db con la app

def insertar_usuarios():
    with app.app_context():
        db.create_all()  # Asegurar que las tablas existen
        # Insertar usuarios
        usuarios = [
            Usuario(nombre_usuario='admin', password='1234', rol_id=1, persona_id=1),
        ]
        
        db.session.add_all(usuarios)
        db.session.commit()
        print("Usuarios insertados correctamente.")

if __name__ == '__main__':
    insertar_usuarios()

