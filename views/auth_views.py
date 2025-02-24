from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app import db
from models import User
from schemas import UserSchema, UserMinimalSchema

auth_bp = Blueprint('auth', __name__)

from base64 import b64decode

@auth_bp.route('/login', methods=['POST'])
def login():
    # Obtener el encabezado Authorization manualmente
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        print("Error: Faltan datos de autorización")
        return jsonify({"Mensaje": "Authorization header missing"}), 400

    # Decodificar el encabezado en formato Basic <base64(username:password)>
    try:
        auth_type, credentials = auth_header.split()
        if auth_type.lower() != 'basic':
            return jsonify({"Mensaje": "Unsupported authorization type"}), 400
        
        # Decodifica las credenciales y separa usuario y contraseña
        decoded_credentials = b64decode(credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")
        print(f"Username recibido: {username}")
        print(f"Password recibido: {password}")

    except Exception as e:
        print("Error al decodificar Authorization:", e)
        return jsonify({"Mensaje": "Invalid authorization format"}), 400

    # Consulta en la base de datos y verifica la autenticación
    usuario = User.query.filter_by(username=username).first()
    print("Usuario encontrado en base de datos:", usuario)

    if usuario and check_password_hash(usuario.password_hash, password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=60),
            additional_claims=dict(
                administrador=usuario.is_admin,
                visor=usuario.is_viewer,
                editor=usuario.is_editor,
            )
        )
        print("Autenticación exitosa")
        return jsonify({'Token': f'Bearer {access_token}'})

    print("Autenticación fallida")
    return jsonify({"Mensaje": "El usuario y la contraseña al parecer no coinciden"}), 401


@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')
    print(administrador)

    if request.method == 'POST':
        if administrador is True:
            print("entre")
            data = request.get_json()
            username = data.get('usuario')
            password = data.get('contrasenia')
            tipo_usuario = data.get('tipo')
            print(tipo_usuario)

            try:
                if tipo_usuario == "admin":
                    is_admin = True
                    is_viewer = False
                    is_editor = False
                elif tipo_usuario == "visor":
                    is_admin = False
                    is_viewer = True
                    is_editor = False
                    print("entre visor")
                elif tipo_usuario == "editor":
                    is_admin = False
                    is_viewer = False
                    is_editor = True

                nuevo_usuario = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    is_admin=is_admin,
                    is_viewer=is_viewer,
                    is_editor=is_editor
                )
                
                db.session.add(nuevo_usuario)
                db.session.commit()
                print("llegue nuevo")
                return jsonify(
                    {
                    "Mensaje":"Usuario creado correctamente",
                    }
                )
            except:
                return jsonify(
                    {
                    "Mensaje":"Fallo la creacion del nuevo usuario",
                    }
                )
        else:
            return jsonify(Mensaje= "Solo el admin puede crear nuevos usuarios")
    
    usuarios = User.query.all()
    if administrador is True:
        return UserSchema().dump(obj=usuarios, many=True)
    else:
        return UserMinimalSchema().dump(obj=usuarios, many=True)
