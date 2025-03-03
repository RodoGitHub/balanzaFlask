from .auth_views import auth_bp
from .balanza_views import balanza_bp
from .clientes_views import clientes_bp
from .facturacion_views import facturacion_bp
from .productos_views import productos_bp
from .rol_views import rol_bp
from .um_views import um_bp



def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(balanza_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(facturacion_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(um_bp)

