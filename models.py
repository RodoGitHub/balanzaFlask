from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime, timezone
from sqlalchemy.sql import func


db = SQLAlchemy()

class UnidadMedida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    productos = db.relationship('Producto', backref='unidad_medida', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=func.now())  # Se guarda la fecha actual automáticamente
    fecha_actualizacion = db.Column(db.DateTime, default=func.now(), onupdate=func.now())  # Se actualiza al modificar
    aplica_descuento = db.Column(db.Boolean, nullable=False, default=True)
    activo_pantalla = db.Column(db.Boolean, nullable=False, default=True)
    imagen_url = db.Column(db.String(255), nullable=True)

    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    
    categoria = db.relationship('Categoria', backref='productos')
    detalles_venta = db.relationship('DetalleVenta', backref='producto', lazy=True)
    
    @validates('precio', 'porcentaje')
    def validate_positive(self, key, value):
        if value < 0:
            raise ValueError(f"{key} debe ser positivo")
        return value

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    contacto = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)

    usuarios = db.relationship('Usuario', backref='persona', lazy=True)
    clientes = db.relationship('Cliente', backref='persona', lazy=True)

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)

    facturas = db.relationship('UsuarioFactura', backref='usuario', lazy=True)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)

    creditos = db.relationship('Credito', backref='cliente', lazy=True)
    ccs = db.relationship('CC', backref='cliente', lazy=True)

class MetodoPago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    facturas = db.relationship('Factura', backref='metodo_pago', lazy=True)

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'), nullable=False)
    
    detalle_venta = db.relationship('DetalleVenta', backref='factura', lazy=True)
    usuario_facturas = db.relationship('UsuarioFactura', backref='factura', lazy=True)
    ccs = db.relationship('CC', backref='factura', lazy=True)
    
    @validates('total')
    def validate_total(self, key, value):
        if value < 0:
            raise ValueError("El total no puede ser negativo")
        return value

class Credito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pago = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    
    @validates('pago')
    def validate_pago(self, key, value):
        if value <= 0:
            raise ValueError("El pago debe ser positivo")
        return value

class CC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
        
    @validates('cantidad')
    def validate_cantidad(self, key, value):
        if value <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return value

class UsuarioFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)