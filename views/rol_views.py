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
def crear_rol():
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
        print("entra")
        roles = Rol.query.all()
        roles_schema = RolSchema(many=True)
        resultado = soles_schema.dump(roles)
        return jsonify({
            "roles": resultado
        }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500