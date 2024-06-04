from flask import render_template, abort ,jsonify, request, make_response, redirect, url_for
from . import bp_auth
from .models import User
from flask_login import current_user, logout_user, login_required, AnonymousUserMixin
from .forms import LoginForm, RegisterForm, SettingsData, SettingsPasswords
import re
from ..utils import email_pattern, validation_auth_errors, validation_login, validation_register
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..utils import verify_user_token, send_email_forgot_password, create_user_token, send_email_active_account

@bp_auth.route('/')
def root():
   return redirect(url_for("auth.auth"))

@bp_auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings_data = SettingsData()
    settings_passwords = SettingsPasswords()
    
    settings_data.fullname.render_kw = {"value": current_user.fullname, "id": "fullname"}
    settings_data.email.render_kw = {"value": current_user.email, "id": "email"}
    if request.method == "POST":
        if settings_data.form_key.data == "form-settings":
            if settings_data.validate_on_submit():
                fullname = settings_data.fullname.data
                profile_picture = settings_data.profile_picture.data
                
                current_user.fullname = fullname
                current_user.profile_picture = profile_picture.filename
                User.save(current_user)
                return make_response(jsonify({'message': "Datos actualizados", 'profile_picture': profile_picture.filename}), 200)  
            
            return make_response(validation_auth_errors(settings_data), 400)  

        elif settings_passwords.form_key.data == "form-password":
            
            if settings_passwords.is_submitted():
                user = User.get_user(current_user.id)
                old_password  = settings_passwords.old_password.data
                new_password = settings_passwords.new_password.data
                repeated_password = settings_passwords.repeat_password.data
                if not User.check_password(user.password, old_password):
                    return make_response(jsonify({'message': "La contraseña antigua no coincide" }), 400)
                elif not (new_password == repeated_password):
                    return make_response(jsonify({'message': "Las nuevas contraseñas no coinciden" }), 400)
                elif User.check_password(user.password, new_password):
                    return make_response(jsonify({'message': "Nueva contraseña igual a la antigua" }), 400)
                user.password = User.hash_password(new_password)
                User.save(user)
                return make_response(jsonify({'message': "Contraseña actualizada"}), 200)  
            
            return make_response(validation_auth_errors(settings_passwords), 400) 
     
    return render_template('settings/settings.html',  
                           settings_data=settings_data, 
                           settings_passwords=settings_passwords,
                           profile_picture=current_user.profile_picture
                           )

@bp_auth.route('/auth', methods=['GET', 'POST'])
def auth():
    login_form = LoginForm()
    register_form = RegisterForm()

    if current_user.is_authenticated:
        return redirect("/chat")
    
    if request.method == "POST":
        if login_form.form_key.data == "form-login":
            return validation_login(login_form)
        elif register_form.form_key.data == "form-register":
            return validation_register(register_form)
                
    elif request.method == "GET":
        return render_template('auth/auth.html', login_form=login_form, register_form=register_form)

# --------------------FORGOT------------------------

@bp_auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Validar el formato del correo electrónico
        if not re.match(email_pattern, email):
            return make_response(jsonify({'message': "Formato de correo electrónico incorrecto"}), 400)

        user = User.get_user_by_email(email)
        if user:
            token = create_user_token(user, 600)        
            send_email_forgot_password(user, token)
            return make_response(jsonify({'message': "Correo electrónico enviado exitosamente."}), 200)
        else:
            return make_response(jsonify({'message': "El correo electrónico no está asociado con ninguna cuenta."}), 400)
    else:
        return render_template('auth/forgot_password.html')


@bp_auth.route('/change-password/<token>', methods=['GET', 'POST'])
def change_password(token):
    user = verify_user_token(token)
    if not user:     
        abort(401)
    
    if request.method == 'POST':
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')
        
        if new_password != confirm_password:
            return make_response(jsonify({'message': "Las contraseñas no coinciden"}), 400)
         
        if User.check_password(user.password, new_password):
            return make_response(jsonify({'message': "Las contraseñas no pueden ser iguales"}), 400)
        
        user.password = User.hash_password(new_password)
        user.save() 
        
        return redirect(url_for('auth.auth'))
    elif request.method == 'GET':
        return render_template('auth/change_password.html', token = token)

# ------------------- FORGOT -----------------------
@bp_auth.route('/active-account/<token>', methods=['GET', 'POST'])
def active_account(token):
    user : User = verify_user_token(token)
    if not user:     
        abort(401)
        
    if request.method == 'POST':
        try:
            send_email_active_account(user, token)
            return make_response(jsonify({'message': "Correo de activación enviado"}), 200)
        except Exception as e:
            return make_response(jsonify({'message': "Error enviando el correo de activación"}), 500)
    elif request.method == 'GET':
        user.active_user()
        user.save()
        return render_template('auth/actived_account.html')


@bp_auth.route('/logout')
def logout():
    user = current_user
    if not isinstance(user, AnonymousUserMixin):
        user.update(authenticated=False)
        logout_user()
    return redirect(url_for('auth.auth'))
