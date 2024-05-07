from flask import Blueprint
bp_chat = Blueprint('chat', __name__, template_folder='../static/templates', static_folder='static/chat')
from . import routes
