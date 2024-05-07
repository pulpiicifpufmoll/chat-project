from flask import Blueprint
bp_admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static/admin')
from . import routes
