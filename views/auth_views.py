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
        
        if not data or not data.get('nombre_usuario') or not data.get('password'):
            return jsonify({"Mensaje": "Faltan datos de autorización"}), 400

        nombre_usuario = data.get('nombre_usuario')
        password = data.get('password')

        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        
        if not usuario:
            return jsonify({"Mensaje": "Usuario no encontrado"}), 401

        if check_password_hash(usuario.password, password):
            access_token = create_access_token(
                identity=nombre_usuario,
                expires_delta=timedelta(days=1),
                additional_claims={
                    'rol_id': usuario.rol_id,
                }
            )
            return jsonify({
                'Token': f'Bearer {access_token}',
                'Mensaje': 'Login exitoso'
            })
        return jsonify({"Mensaje": "Contraseña incorrecta"}), 401
    
    except Exception as e:
        print("Error en login:", str(e))
        return jsonify({"Mensaje": "Error interno del servidor"}), 500

@auth_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    try:
        if request.method == 'POST':
            claims = get_jwt()
            rol_id = claims.get('rol_id')
            if rol_id != 1:
                return jsonify({"Mensaje": "Solo el administrador puede crear usuarios"}), 403

            data = request.get_json()

            if not all(key in data for key in ['nombre_usuario', 'password', 'rol_id', 'persona_id']):
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
                return jsonify({
                    "Mensaje": "Usuario creado correctamente",
                    "usuario": data['nombre_usuario']
                }), 201
            
            except Exception as e:
                db.session.rollback()
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

@auth_bp.route('/users/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_user(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        if rol_id != 1:
            return jsonify({"Mensaje": "Solo el administrador puede eliminar usuarios"}), 403
        
        usuario = Usuario.query.get(id)
        
        if not usuario:
            return jsonify({"Mensaje": "Usuario no encontrado"}), 404
        
        nombre_usuario = usuario.nombre_usuario
        
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({
            "Mensaje": "Usuario eliminado correctamente",
            "usuario": nombre_usuario,
            "id": id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al eliminar el usuario",
            "error": str(e)
        }), 500

@auth_bp.route('/users/<int:id>/editar', methods=['POST'])
@jwt_required()
def change_password(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({"Mensaje": "Usuario no encontrado"}), 404

        # Verificar permisos (solo admin o el mismo usuario)
        if rol_id != 1:
            return jsonify({
                "Mensaje": "No tiene permisos para cambiar esta contraseña"
            }), 403

        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({
                "Mensaje": "Falta la nueva contraseña"
            }), 400

        # Actualizar la contraseña
        usuario.password = generate_password_hash(data['password'])
        db.session.commit()

        return jsonify({
            "Mensaje": "Contraseña actualizada correctamente",
            "usuario": usuario.nombre_usuario
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error al cambiar contraseña: {str(e)}")
        return jsonify({
            "Mensaje": "Error al cambiar la contraseña",
            "error": str(e)
        }), 500