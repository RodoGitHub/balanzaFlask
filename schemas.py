from marshmallow import Schema, fields, validates, ValidationError, post_dump
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class UnidadMedidaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    precio = fields.Float(required=True)
    porcentaje = fields.Float(required=True)
    fecha_creacion = fields.DateTime(dump_only=True)
    fecha_actualizacion = fields.DateTime(dump_only=True)
    unidad_medida_id = fields.Int(required=True)
    categoria_id = fields.Int(required=True)
    aplica_descuento = fields.Boolean()

    @post_dump
    def adjust_dates(self, data, **kwargs):
        argentina_tz = ZoneInfo("America/Argentina/Buenos_Aires")
        
        if 'fecha_creacion' in data and data['fecha_creacion']:
            fecha_utc = datetime.fromisoformat(data['fecha_creacion'])
            if fecha_utc.tzinfo is None:  # Si la fecha no tiene zona horaria
                fecha_utc = fecha_utc.replace(tzinfo=timezone.utc)
            fecha_arg = fecha_utc.astimezone(argentina_tz)
            data['fecha_creacion'] = fecha_arg.strftime("%Y-%m-%d %H:%M:%S")
            
        if 'fecha_actualizacion' in data and data['fecha_actualizacion']:
            fecha_utc = datetime.fromisoformat(data['fecha_actualizacion'])
            if fecha_utc.tzinfo is None:  # Si la fecha no tiene zona horaria
                fecha_utc = fecha_utc.replace(tzinfo=timezone.utc)
            fecha_arg = fecha_utc.astimezone(argentina_tz)
            data['fecha_actualizacion'] = fecha_arg.strftime("%Y-%m-%d %H:%M:%S")
            
        return data

    @validates("precio")
    def validate_precio(self, value):
        if value <= 0:
            raise ValidationError("El precio debe ser mayor a 0")

    @validates("porcentaje")
    def validate_porcentaje(self, value):
        if value < 0:
            raise ValidationError("El porcentaje no puede ser negativo")

class PersonaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    contacto = fields.Str(required=True)
    direccion = fields.Str(required=True)

class RolSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_usuario = fields.Str(required=True)
    rol_id = fields.Int(required=True)
    persona_id = fields.Int(required=True)
    password = fields.Str(required=True, load_only=True)

class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    persona_id = fields.Int(required=True)

class MetodoPagoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)

class FacturaSchema(Schema):
    id = fields.Int(dump_only=True)
    total = fields.Float(required=True)
    metodo_pago_id = fields.Int(required=True)
    fecha = fields.DateTime(dump_only=True)
    detalle_venta_id = fields.Int(required=True)

class CreditoSchema(Schema):
    id = fields.Int(dump_only=True)
    cliente_id = fields.Int(required=True)
    pago = fields.Float(required=True)
    fecha = fields.DateTime(dump_only=True)

class CCSchema(Schema):
    id = fields.Int(dump_only=True)
    cliente_id = fields.Int(required=True)
    factura_id = fields.Int(required=True)
    fecha = fields.DateTime(dump_only=True)

class DetalleVentaSchema(Schema):
    id = fields.Int(dump_only=True)
    producto_id = fields.Int(required=True)
    cantidad = fields.Int(required=True)
    fecha = fields.DateTime(dump_only=True)

class UsuarioFacturaSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario_id = fields.Int(required=True)
    factura_id = fields.Int(required=True)

