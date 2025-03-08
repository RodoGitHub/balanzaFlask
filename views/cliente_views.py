from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import Cliente
from schemas import ClienteSchema

cliente_bp = Blueprint('clientes', __name__)

@cliente_bp.route('/cliente', methods=['GET','POST'])
@jwt_required()
def cliente():
    try:
        if request.method == 'POST':
            claims = get_jwt()
            rol_id = claims.get('rol_id')
            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para crear Clientes"})
            data = request.get_json()

            if not data:
                return jsonify({"mensaje": "Debe ingresar una Persona"})
            
            try:
                nuevo_cliente = Cliente(
                    persona_id=data['persona_id']
                )

                db.session.add(nuevo_cliente)
                db.session.commit()
                return jsonify({"mensaje": "Cliente creado exitosamente"}), 201

            except Exception as e:
                return jsonify({"mensaje": "Error al crear el Cliente"}), 500

        cliente = Cliente.query.all()
        cliente_schema = ClienteSchema(many=True)
        resultado = cliente_schema.dump(cliente)
        if not resultado:
            return jsonify({"mensaje": "No existen registros"})
        else:
            return jsonify({
                "um": resultado
            }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@cliente_bp.route('/cliente/<int:id>/delete', methods=['POST'])
@jwt_required()
def cliente_um(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')

        if rol_id != 1:
            return jsonify({"mesnaje": "Solo el administrador puede eliminar"})
    
        cliente = Cliente.query.get(id)

        if not Cliente:
            return jsonify({"mensaje": "Cliente no encontrado"})

        db.session.delete(cliente)
        db.session.commit()

        return jsonify({"mensaje": "Cliente eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "mensaje": "Error al eliminar Cliente",
            "error": str(e)
            }), 500