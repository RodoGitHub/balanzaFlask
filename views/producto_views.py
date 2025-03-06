from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import Producto
from schemas import ProductoSchema

producto_bp = Blueprint('productos', __name__)

@producto_bp.route('/producto', methods=['GET','POST'])
@jwt_required()
def producto():
    try:
        if request.method == 'POST':
            claims = get_jwt()
            rol_id = claims.get('rol_id')
            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para esta seccion"})
            data = request.get_json()

            if not data or not data.get('nombre') or not data.get('precio') or not data.get('porcentaje') or not data.get('unidad_medida_id') or not data.get('categoria_id'):
                return jsonify({"mensaje": "Debe llenar todos los campos"})
                
            print("entra")
            try:
                nuevo_producto = Producto(
                    nombre=data['nombre'],
                    precio=data['precio'],
                    porcentaje=data['porcentaje'],
                    unidad_medida_id=data['unidad_medida_id'],
                    categoria_id=data['categoria_id']
                )

                db.session.add(nuevo_producto)
                db.session.commit()
                return jsonify({"mensaje": "Creado exitosamente"}), 201

            except Exception as e:
                return jsonify({
                    "mensaje": "Error al crear",
                    "error": str(e)
                }), 500

        producto = Producto.query.all()
        producto_schema = ProductoSchema(many=True)
        resultado = producto_schema.dump(producto)
        if not resultado:
            return jsonify({"mensaje": "No existen registros"})
        else:
            return jsonify({
                "Producto": resultado
            }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@producto_bp.route('/producto/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_producto(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        if rol_id != 1:
            return jsonify({"Mensaje": "Solo el administrador puede eliminar"}), 403
        
        producto = Producto.query.get(id)
        
        if not producto:
            return jsonify({"Mensaje": "No se encuentra el producto"}), 404
        
        db.session.delete(producto)
        db.session.commit()
        
        return jsonify({
            "Mensaje": "Se elimino correctamente",
            "Persona": producto.nombre,
            "id": id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al eliminar al eliminar",
            "error": str(e)
        }), 500