from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime, timezone

db = SQLAlchemy()

class UnidadMedida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    productos = db.relationship('Producto', backref='unidad_medida', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

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
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

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
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    detalle_venta_id = db.Column(db.Integer, db.ForeignKey('detalle_venta.id'), nullable=False)

    usuario_facturas = db.relationship('UsuarioFactura', backref='factura', lazy=True)
    ccs = db.relationship('CC', backref='factura', lazy=True)

class Credito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pago = db.Column(db.Float, nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

class CC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)

    facturas = db.relationship('Factura', backref='detalle_venta', lazy=True)

class UsuarioFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)