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
from models import Rol
from schemas import RolSchema

rol_bp = Blueprint('rol', __name__)

@rol_bp.route('/roles', methods=['GET', 'POST'])
@jwt_required()
def crear_ver_roles():
    try:
        if request.method == 'POST':
            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para crear roles"})
            data = request.get.json()

            if not data or not data.get('nombre'):
                return jsonify({"mensaje": "Debe ingresar un nombre"})
            
            try:
                nuevo_rol = Rol(
                    nombre=data['nombre']
                )

                db.session.add(nuevo_rol)
                db.session.commit()
                return jsonify({"mensaje": "Rol creado exitosamente"}), 201

            except Excepcion as e:
                return jsonify({"mensaje": "Error al crear el rol"}), 500

        roles = Rol.query.all()
        roles_schema = RolSchema(many=True)
        resultado = roles_schema.dump(roles)
        return jsonify({
            "roles": resultado
        }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@rol_bp.route('/roles/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_rol(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')

        if rol_id != 1:
            return jsonify({"mesnaje": "Solo el administrador puede eliminar los Roles"})
    
        roles = Rol.query.get(id)

        if not roles:
            return jsonify({"mensaje": "Rol no encontrado"})

        db.session.delete(roles)
        db.session.commit()

        return jsonify({"mensaje": "Rol eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "mensaje": "Error al eliminar el Rol",
            "error": str(e)
            }), 500

