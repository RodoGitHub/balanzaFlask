from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import Categoria
from schemas import CategoriaSchema

categoria_bp = Blueprint('categorias', __name__)

@categoria_bp.route('/categoria', methods=['GET','POST'])
@jwt_required()
def categoria():
    try:
        if request.method == 'POST':

            claims = get_jwt()
            rol_id = claims.get('rol_id')

            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para crear"})
            data = request.get_json()

            if not data or not data.get('nombre'):
                return jsonify({"mensaje": "Debe llenar todos los campos"})
            
            try:
                nueva_categoria = Categoria(
                    nombre=data['nombre']
                )

                db.session.add(nueva_categoria)
                db.session.commit()
                return jsonify({"mensaje": "Creada exitosamente"}), 201

            except Exception as e:
                return jsonify({"mensaje": "Error al crear"}), 500

        categoria = Categoria.query.all()
        categoria_schema = CategoriaSchema(many=True)
        resultado = categoria_schema.dump(categoria)
        if not resultado:
            return jsonify({"mensaje": "No existen registros"})
        else:
            return jsonify({
                "Categorias": resultado
            }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@categoria_bp.route('/categoria/<int:id>/editar', methods=['POST'])
@jwt_required()
def editar_categoria(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        categoria = Categoria.query.get(id)
        if not categoria:
            return jsonify({"Mensaje": "No se encontro la categoria"}), 404

        if rol_id != 1:
            return jsonify({
                "Mensaje": "No tiene permisos para editar"
            }), 403

        data = request.get_json()
        if not data:
            return jsonify({
                "Mensaje": "Por favor llenar todos los campos"
            }), 400

        categoria.nombre = data['nombre']

        db.session.commit()

        return jsonify({
            "Mensaje": "Datos actualizados correctamente",
            "Persona": categoria.nombre
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al actualizar datos",
            "error": str(e)
        }), 500

@categoria_bp.route('/categoria/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_categoria(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        if rol_id != 1:
            return jsonify({"Mensaje": "Solo el administrador puede eliminar"}), 403
        
        categoria = Categoria.query.get(id)
        
        if not categoria:
            return jsonify({"Mensaje": "No se encuentra categoria"}), 404
        
        db.session.delete(categoria)
        db.session.commit()
        
        return jsonify({
            "Mensaje": "Se elimino correctamente",
            "Persona": categoria.nombre,
            "id": id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al eliminar el usuario",
            "error": str(e)
        }), 500