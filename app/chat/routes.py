from flask import render_template, request
from . import bp_chat
from flask_login import current_user, login_required
from app.auth.utils import admin_required


@bp_chat.route('/chat', methods=['GET'])
@login_required
def chat():
    
    if request.method == "POST":
        pass
    return render_template('chat/chat.html', current_user=current_user)


@bp_chat.route('/chat/completions')
@admin_required
@login_required
def completions():
    pass

@bp_chat.route('/chat/chunks', methods=['POST'])
@admin_required
@login_required
def chunks():
    pass
