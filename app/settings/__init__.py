from flask import Blueprint
bp_settings = Blueprint('settings', __name__, template_folder='../static/templates', static_folder='static')
from . import routes
