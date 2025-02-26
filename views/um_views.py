from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import UnidadMedida
from schemas import UnidadMedidaSchema

um_bp = Blueprint('unidad_de_medidas', __name__)

@productos_bp.route('/um', methods=['GET','POST'])
@jwt_required()
def um():
    um = UnidadMedida.query.filter_by(activo=True).all()

    additional_data = get_jwt()
    admin = additional_data.get('administrador')

    if request.method == 'POST':
        if  admin:
            data = request.get_json()
            errors = UnidadMedidaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors))
            
            nueva_um = UnidadMedida(
                nombre=data.get('nombre'),
            )
            db.session.add(nueva_um)
            db.session.commit()
            return UnidadMedidaSchema().dump(nueva_um), 201
        else:
            return jsonify(Mensaje= "Solo el admin puede crear nuevas UM")
    
    if visor or admin:
        return UnidadMedidaSchema().dump(um, many=True)
    return jsonify(Mensaje="El usuario no tiene permiso")