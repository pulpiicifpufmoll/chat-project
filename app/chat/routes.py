from flask import render_template, json, request, make_response, jsonify
from . import bp_chat
from flask_login import current_user, login_required

@bp_chat.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == "POST":
        pass
    return render_template('chat/chat.html', current_user=current_user)
