from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

from app import db
from models import Producto
from schemas import ProductoSchema

producto_bp = Blueprint('productos', __name__)

# Ruta de imagen predeterminada para productos sin imagen
DEFAULT_PRODUCT_IMAGE = '/static/images/productos/noimagen.png'  # Ajusta esto a tu imagen predeterminada

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para guardar el archivo de imagen o retornar imagen predefinida
def save_image(file):
    try:
        # Si no hay archivo o el archivo está vacío, retornar la imagen predeterminada
        if not file or file.filename == '':
            return DEFAULT_PRODUCT_IMAGE
            
        if allowed_file(file.filename):
            # Crear nombre de archivo único para evitar colisiones
            filename = secure_filename(file.filename)
            # Extraer extensión
            ext = filename.rsplit('.', 1)[1].lower()
            # Crear nombre único
            unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            
            # Asegurarse de que el directorio existe
            upload_folder = os.path.join(current_app.static_folder, 'uploads', 'productos')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Guardar el archivo
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # Devolver la ruta relativa para almacenar en la BD
            return f'/static/uploads/productos/{unique_filename}'
        
        # Si la extensión no es permitida, usar la imagen predeterminada
        return DEFAULT_PRODUCT_IMAGE
        
    except Exception as e:
        print(f"Error al guardar imagen: {str(e)}")
        return DEFAULT_PRODUCT_IMAGE

@producto_bp.route('/producto', methods=['POST'])
@jwt_required()
def crear_producto():
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        if rol_id != 1:
            return jsonify({"mensaje": "No tienes permisos para esta sección"}), 403
        
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        porcentaje = request.form.get('porcentaje', 0)
        unidad_medida_id = request.form.get('unidad_medida_id')
        categoria_id = request.form.get('categoria_id')
        aplica_descuento = request.form.get('aplica_descuento', 'false').lower() == 'true'
        activo_pantalla = request.form.get('activo_pantalla', 'true').lower() == 'true'
        
        if not all([nombre, precio, unidad_medida_id, categoria_id]):
            return jsonify({"mensaje": "Debe llenar todos los campos requeridos"}), 400
        
        imagen_url = save_image(request.files.get('imagen', None))
        
        try:
            nuevo_producto = Producto(
                nombre=nombre,
                precio=float(precio),
                porcentaje=float(porcentaje),
                aplica_descuento=aplica_descuento,
                unidad_medida_id=int(unidad_medida_id),
                categoria_id=int(categoria_id),
                activo_pantalla=activo_pantalla,
                imagen_url=imagen_url
            )

            db.session.add(nuevo_producto)
            db.session.commit()
            return jsonify({"mensaje": "Creado exitosamente", "producto_id": nuevo_producto.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "mensaje": "Error al crear",
                "error": str(e)
            }), 500

    except Exception as e:
        return jsonify({"mensaje": f"Error interno del servidor: {str(e)}"}), 500


@producto_bp.route('/producto', methods=['GET'])
def obtener_productos():
    try:
        # Esta función no requiere jwt_required() para permitir acceso público
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
        return jsonify({"mensaje": f"Error interno del servidor: {str(e)}"}), 500


@producto_bp.route('/producto/<int:id>/editar', methods=['POST'])
@jwt_required()
def editar_producto(id):
    try:
        claims = get_jwt()
        rol_id = claims.get('rol_id')
        
        producto = Producto.query.get(id)
        if not producto:
            return jsonify({"Mensaje": "No se encontró el producto"}), 404

        if rol_id != 1:
            return jsonify({
                "Mensaje": "No tiene permisos para editar"
            }), 403

        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        porcentaje = request.form.get('porcentaje')
        unidad_medida_id = request.form.get('unidad_medida_id')
        categoria_id = request.form.get('categoria_id')
        aplica_descuento = request.form.get('aplica_descuento', 'false').lower() == 'true'
        activo_pantalla = request.form.get('activo_pantalla', 'true').lower() == 'true'
        
        if nombre:
            producto.nombre = nombre
        if precio:
            producto.precio = float(precio)
        if porcentaje:
            producto.porcentaje = float(porcentaje)
        if unidad_medida_id:
            producto.unidad_medida_id = int(unidad_medida_id)
        if categoria_id:
            producto.categoria_id = int(categoria_id)
            
        producto.aplica_descuento = aplica_descuento
        producto.activo_pantalla = activo_pantalla

        # Procesar imagen si hay una nueva
        if 'imagen' in request.files and request.files['imagen'].filename:
            nueva_imagen_url = save_image(request.files['imagen'])
            if nueva_imagen_url:
                # Opcional: borrar imagen anterior si no es la predeterminada
                if producto.imagen_url and producto.imagen_url != DEFAULT_PRODUCT_IMAGE:
                    try:
                        # Ruta absoluta del archivo
                        archivo_antiguo = os.path.join(current_app.root_path, producto.imagen_url.lstrip('/'))
                        if os.path.exists(archivo_antiguo):
                            os.remove(archivo_antiguo)
                    except Exception as e:
                        print(f"Error al eliminar imagen antigua: {str(e)}")
                
                producto.imagen_url = nueva_imagen_url

        db.session.commit()

        return jsonify({
            "Mensaje": "Datos actualizados correctamente",
            "Producto": producto.nombre
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "Mensaje": "Error al actualizar datos",
            "error": str(e)
        }), 500


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
        
        # Eliminar la imagen asociada si existe y no es la predeterminada
        if producto.imagen_url and producto.imagen_url != DEFAULT_PRODUCT_IMAGE:
            try:
                archivo = os.path.join(current_app.root_path, producto.imagen_url.lstrip('/'))
                if os.path.exists(archivo):
                    os.remove(archivo)
            except Exception as e:
                print(f"Error al eliminar imagen: {str(e)}")
        
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
            "Mensaje": "Error al eliminar",
            "error": str(e)
        }), 500