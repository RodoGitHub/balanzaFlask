from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import MetodoPago
from schemas import MetodoPagoSchema

metodopago_bp = Blueprint('metodopago', __name__)

@metodopago_bp.route('/metodopago', methods=['GET','POST'])
@jwt_required()
def metodopago():
    try:
        if request.method == 'POST':
            claims = get_jwt()
            rol_id = claims.get('rol_id')
            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para crear"})
            data = request.get_json()

            if not data:
                return jsonify({"mensaje": "Debe ingresar un nombre"})
            
            try:
                nuevo_metodopago = MetodoPago(
                    nombre=data['nombre']
                )

                db.session.add(nuevo_metodopago)
                db.session.commit()
                return jsonify({"mensaje": "Creada exitosamente"}), 201

            except Exception as e:
                return jsonify({"mensaje": "Error al crear"}), 500

        metodopago = MetodoPago.query.all()
        metodopago_schema = MetodoPagoSchema(many=True)
        resultado = metodopago_schema.dump(metodopago)
        if not resultado:
            return jsonify({"mensaje": "No existen registros"})
        else:
            return jsonify({
                "um": resultado
            }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@metodopago_bp.route('/metodopago/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_metodopago(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')

        if rol_id != 1:
            return jsonify({"mesnaje": "Solo el administrador puede eliminar"})
    
        metodopago = MetodoPago.query.get(id)

        if not metodopago:
            return jsonify({"mensaje": "metodopago no encontrado"})

        db.session.delete(metodopago)
        db.session.commit()

        return jsonify({"mensaje": "eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "mensaje": "Error al eliminar",
            "error": str(e)
            }), 500