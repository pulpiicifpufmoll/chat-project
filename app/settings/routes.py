from . import bp_settings
from flask import render_template, current_app ,make_response, request, jsonify, send_file
from flask_login import login_required, current_user
from ..forms import SettingsData, SettingsPasswords
from app.models import User
from ..utils import validation_auth_errors, createUserInfoJson, validateSettingsData, validateSettingsPasswords

@bp_settings.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings_data = SettingsData()
    settings_passwords = SettingsPasswords()
    
    settings_data.fullname.render_kw = {"value": current_user.fullname, "id": "fullname"}
    settings_data.email.render_kw = {"value": current_user.email, "id": "email"}
    if request.method == "POST":
        if settings_data.form_key.data == "form-settings":
            if validateSettingsData(settings_data):
                return make_response(jsonify({'message': "Datos actualizados", 'profile_picture': settings_data.profile_picture.data.filename}), 200)  
            else:
                return make_response(validation_auth_errors(settings_data), 400)  

        elif settings_passwords.form_key.data == "form-password":
            
           if validateSettingsPasswords(settings_passwords):
               return make_response(jsonify({'message': "Contraseña actualizada"}), 200)  
           else:
               return make_response(validation_auth_errors(settings_passwords), 400) 
     
    return render_template('settings/settings.html',  
                           settings_data=settings_data, 
                           settings_passwords=settings_passwords,
                           profile_picture=current_user.profile_picture
                           )
    
@bp_settings.route('/user-info', methods=['GET'])
@login_required
def userinfo():
    user : User = createUserInfoJson(current_user.id)
    return make_response({'user_info': user}, 200)
