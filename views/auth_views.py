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
from models import Usuario
from schemas import UsuarioSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)
        
        if not data or not data.get('nombre_usuario') or not data.get('password'):
            return jsonify({"Mensaje": "Faltan datos de autorización"}), 400

        nombre_usuario = data.get('nombre_usuario')
        password = data.get('password')
        print(f"Username recibido: {nombre_usuario}")
        print(f"Password recibido: {password}")

        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        
        if not usuario:
            print(f"Usuario {nombre_usuario} no encontrado")
            return jsonify({"Mensaje": "Usuario no encontrado"}), 401
            
        print("Usuario encontrado:", usuario)
        print("Password almacenado (hash):", usuario.password)

        if check_password_hash(usuario.password, password):
            access_token = create_access_token(
                identity=nombre_usuario,
                expires_delta=timedelta(minutes=60),
                additional_claims={
                    'rol_id': usuario.rol_id,
                }
            )
            print("Autenticación exitosa para usuario:", nombre_usuario)
            return jsonify({
                'Token': f'Bearer {access_token}',
                'Mensaje': 'Login exitoso'
            })

        print("Password incorrecto para usuario:", nombre_usuario)
        return jsonify({"Mensaje": "Contraseña incorrecta"}), 401
    
    except Exception as e:
        print("Error en login:", str(e))
        return jsonify({"Mensaje": "Error interno del servidor"}), 500

@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    try:
        if request.method == 'POST':
            if rol_id != 1:
                print("Intento de crear usuario sin permisos de administrador")
                return jsonify({"Mensaje": "Solo el administrador puede crear usuarios"}), 403

            data = request.get_json()
            print("Datos recibidos para crear usuario:", data)

            if not all(key in data for key in ['nombre_usuario', 'password', 'rol_id', 'persona_id']):
                print("Faltan datos en la petición")
                return jsonify({"Mensaje": "Faltan datos requeridos"}), 400

            try:
                nuevo_usuario = Usuario(
                    nombre_usuario=data['nombre_usuario'],
                    password=generate_password_hash(data['password']),
                    rol_id=data['rol_id'],
                    persona_id=data['persona_id']
                )
                
                db.session.add(nuevo_usuario)
                db.session.commit()
                print(f"Usuario {data['nombre_usuario']} creado exitosamente")
                return jsonify({
                    "Mensaje": "Usuario creado correctamente",
                    "usuario": data['nombre_usuario']
                }), 201
            
            except Exception as e:
                db.session.rollback()
                print("Error al crear usuario:", str(e))
                return jsonify({
                    "Mensaje": "Error al crear el usuario",
                    "error": str(e)
                }), 500

        usuarios = Usuario.query.all()
        usuarios_schema = UsuarioSchema(many=True)
        resultado = usuarios_schema.dump(usuarios)
        return jsonify({
            "usuarios": resultado
        }), 200

    except Exception as e:
        return jsonify({"Mensaje": "Error interno del servidor"}), 500