from flask import Blueprint
bp_auth = Blueprint('auth', __name__, template_folder='../static/templates', static_folder='static/auth')
from . import routes
