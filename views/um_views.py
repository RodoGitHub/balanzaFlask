from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import UnidadMedida
from schemas import UnidadMedidaSchema

um_bp = Blueprint('unidad_de_medidas', __name__)

@um_bp.route('/um', methods=['GET','POST'])
@jwt_required()
def um():
    try:
        if request.method == 'POST':
            claims = get_jwt()
            rol_id = claims.get('rol_id')
            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para crear Unidades de medida"})
            data = request.get_json()

            if not data or not data.get('nombre'):
                return jsonify({"mensaje": "Debe ingresar un nombre"})
            
            try:
                nueva_um = UnidadMedida(
                    nombre=data['nombre']
                )

                db.session.add(nueva_um)
                db.session.commit()
                return jsonify({"mensaje": "UM creada exitosamente"}), 201

            except Exception as e:
                return jsonify({"mensaje": "Error al crear el UM"}), 500

        um = UnidadMedida.query.all()
        um_schema = UnidadMedidaSchema(many=True)
        resultado = um_schema.dump(um)
        if not resultado:
            return jsonify({"mensaje": "No existen registros"})
        else:
            return jsonify({
                "um": resultado
            }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@um_bp.route('/um/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_um(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')

        if rol_id != 1:
            return jsonify({"mesnaje": "Solo el administrador puede eliminar las UM"})
    
        um = UnidadMedida.query.get(id)

        if not um:
            return jsonify({"mensaje": "UM no encontrado"})

        db.session.delete(um)
        db.session.commit()

        return jsonify({"mensaje": "UM eliminado correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "mensaje": "Error al eliminar la UM",
            "error": str(e)
            }), 500