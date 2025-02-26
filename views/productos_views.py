from flask import Blueprint, request, jsonify, make_response

from flask_jwt_extended import (
    get_jwt, 
    jwt_required
    )

from app import db
from models import Producto
from schemas import ProductoSchema

productos_bp = Blueprint('productos', __name__)
