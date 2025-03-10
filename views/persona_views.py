from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import Persona
from schemas import PersonaSchema

persona_bp = Blueprint('personas', __name__)

@persona_bp.route('/persona', methods=['GET','POST'])
@jwt_required()
def persona():
    try:
        if request.method == 'POST':
            claims = get_jwt()
            rol_id = claims.get('rol_id')
            if rol_id != 1:
                return jsonify({"mensaje": "No tienes permisos para crear Personas"})
            data = request.get_json()

            if not data or not data.get('nombre') or not data.get('contacto') or not data.get('direccion'):
                return jsonify({"mensaje": "Debe llenar todos los campos"})
            
            try:
                nueva_persona = Persona(
                    nombre=data['nombre'],
                    contacto=data['contacto'],
                    direccion=data['direccion']
                )

                db.session.add(nueva_persona)
                db.session.commit()
                return jsonify({"mensaje": "Persona creada exitosamente"}), 201

            except Exception as e:
                return jsonify({"mensaje": "Error al crear el Persona"}), 500

        persona = Persona.query.all()
        persona_schema = PersonaSchema(many=True)
        resultado = persona_schema.dump(persona)
        if not resultado:
            return jsonify({"mensaje": "No existen registros"})
        else:
            return jsonify({
                "persona": resultado
            }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@persona_bp.route('/persona/<int:id>/editar', methods=['POST'])
@jwt_required()
def editar_persona(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        persona = Persona.query.get(id)
        if not persona:
            return jsonify({"Mensaje": "No se encontro la persona"}), 404

        if rol_id != 1:
            return jsonify({
                "Mensaje": "No tiene permisos para editar"
            }), 403

        data = request.get_json()
        if not data:
            return jsonify({
                "Mensaje": "Por favor llenar todos los campos"
            }), 400

        persona.nombre = data['nombre']
        persona.contacto = data['contacto']
        persona.direccion = data['direccion']

        db.session.commit()

        return jsonify({
            "Mensaje": "Datos actualizados correctamente",
            "Persona": persona.nombre
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al actualizar datos",
            "error": str(e)
        }), 500

@persona_bp.route('/persona/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_persona(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        if rol_id != 1:
            return jsonify({"Mensaje": "Solo el administrador puede eliminar personas"}), 403
        
        persona = Persona.query.get(id)
        
        if not persona:
            return jsonify({"Mensaje": "No se encuentra la persona"}), 404
        
        db.session.delete(persona)
        db.session.commit()
        
        return jsonify({
            "Mensaje": "Se elimino correctamente",
            "Persona": persona.nombre,
            "id": id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al eliminar el usuario",
            "error": str(e)
        }), 500