from .auth_views import auth_bp
from .balanza_views import balanza_bp
from .cliente_views import cliente_bp
from .facturacion_views import facturacion_bp
from .rol_views import rol_bp
from .um_views import um_bp
from .persona_views import persona_bp
from .categoria_views import categoria_bp
from .producto_views import producto_bp
from .metodopago_views import metodopago_bp


def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(balanza_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(facturacion_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(um_bp)
    app.register_blueprint(persona_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(metodopago_bp)