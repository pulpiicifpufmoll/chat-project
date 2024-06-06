from functools import wraps
from flask import abort, make_response, jsonify, url_for, current_app
from flask_login import current_user, login_user
from .models import User
import re
from datetime import datetime
from flask_principal import identity_changed, Identity, AnonymousIdentity
from time import time
from app import mail
from flask_mail import Message
import jwt, os

#Declaramos una variable con las restricciones del formato del email.
# email_pattern = r'^[a-zA-Z0-9._%+-]+@angel24\.com$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

def get_email_corporation(email):
    parts = email.split('@')
    if len(parts) == 2:
        return parts[1]
    else:
        return None

def createUserInfoJson(user_id):
    user : User = User.get_user(user_id)
    return {
        'user_id': user.id,
        'username': user.fullname,
        'email': user.email,
        'profile_picture': user.profile_picture
    }

# --------------------LOGIN------------------------

def validation_login(form):
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.get_user_by_email(email)
        
        if user is not None and User.check_password(user.password, password):
            if not user.is_active():
                return make_response(jsonify({'message': 'La cuenta de correo aún no está verificada'}), 400)
            user.authenticated = True
            user.save()
            
            login_user(user)
            
            # Se establece el rol 'user' para el usuario     
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return make_response(jsonify({'user': user.toJson()}), 200)
        
        elif user is None:
            return make_response(jsonify({'errorType': "email_not_found", 'message': "Email no encontrado"}), 400)
        else:
            return make_response(jsonify({'errorType': "incorrect_password", 'message': "Contraseña incorrecta"}), 400)
    else:
        return validation_auth_errors(form)


# --------------------REGISTER------------------------

def validation_register(form):
    if form.validate_on_submit():
        fullname = form.fullname.data
        email = form.email.data
        password = form.password.data
        password_confirm = form.password_confirm.data

        # if get_email_corporation(email) != "angel24.com":
        #     return make_response(jsonify({'message': "Solo se permiten correos de nuestra corporativa"}), 400)

        user = User.get_user_by_email(email)
        if user is not None:
            return make_response(jsonify({'message': "Este correo ya está en uso"}), 400)

        elif not re.match(email_pattern, email):
            return make_response(jsonify({'message': "Formato de correo electrónico incorrecto"}), 400)
     
        elif password != password_confirm:
            return make_response(jsonify({'message': "Las contraseñas no coinciden"}), 400)

        user = User(fullname=fullname, email=email, password=User.hash_password(password), create_date=datetime.now(), role='user')
        
        User.save(user)
        
        active_account_token = create_user_token(user, 86400) #24 horas para expirar
        send_email_active_account(user, active_account_token)
        
        return make_response(jsonify({'message': "Usuario creado exitosamente, le hemos enviado un correo para darle de alta"}), 200)
    
    else:
        return validation_auth_errors(form)

# ----------------- SETTINGS ----------------------
def uploadPicture(file):
    if os.path.exists(current_app.config['PICTURES_FOLDER'] + file.filename):
        return 'El archivo ya existe', 400
    file.save(os.path.join(current_app.config['PICTURES_FOLDER'], file.filename))

def validateSettingsData(settings_data):
        if settings_data.validate_on_submit():
            fullname = settings_data.fullname.data
            profile_picture = settings_data.profile_picture.data
            if profile_picture.filename != "":
                uploadPicture(profile_picture)
                current_user.profile_picture = profile_picture.filename
            if fullname == "":
                return make_response(jsonify({'message': "El nombre de usuario no puede estar vacío" }), 400)
            current_user.fullname = fullname
            User.save(current_user)
            return True

def validateSettingsPasswords(settings_passwords):
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
        return True

# ------------------- ERRORS -----------------------

def validation_auth_errors(form):
    if 'email' in form.errors:
        return make_response(jsonify({'message': "Formato de correo electrónico incorrecto"}), 400)
    elif 'password' in form.errors or 'password_confirm' in form.errors:
        return make_response(jsonify({'message': "Las contraseñas no coinciden"}), 400)
    elif 'fullname' in form.errors:
        return make_response(jsonify({'message': "Formato no válido para el nombre"}), 400)
    return make_response(jsonify({'message': "Ocurrió un error al procesar el formulario"}), 400)

# ------------------- MAILING ----------------------

def create_user_token(user, expires):
    try:
        payload = {
            'user_email':user.email,
            'exp': time() + expires 
        }

        secret_key = os.getenv('SECRET_KEY')
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    except Exception as e:
        print("Error al codificar el token JWT:", e)

    return None

def verify_user_token(token):
    secret_key = os.getenv('SECRET_KEY')
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_email = payload['user_email']
        return User.get_user_by_email(user_email)
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, KeyError):
        return None
    
def send_email_forgot_password(user, token):
    subject = "Restablecer Contraseña"
    sender_email = "angel24@gmail.com" 
    recipient_email = user.email
    
    message_body = f"""
    
    Hola {user.fullname},

    Recibiste este correo electrónico porque solicitaste un restablecimiento de contraseña para tu cuenta en nuestro sitio web.

    Por favor, haz clic en el siguiente enlace para restablecer tu contraseña:

    {url_for('auth.change_password', token=token, _external=True)}

        Si no solicitaste este restablecimiento de contraseña, simplemente ignora este correo electrónico.

        Gracias,

        Tu equipo de soporte, Angel24.
        
    """

    # Crear el objeto Message para el correo electrónico
    msg = Message(subject, sender=sender_email, recipients=[recipient_email])
    msg.body = message_body
    mail.send(msg)

def send_email_active_account(user, token):
    subject = "Activación de cuenta"
    sender_email = "pulpii.assists@gmail.com" 
    recipient_email = user.email
    
    message_body = f"""
    
    Hola {user.fullname},

    Te damos la bienvenida a tu nuevo chat corporativo. Para comenzar a disfrutar de nuestro servicio, necesitamos que actives tu cuenta.

    Haz clic en el siguiente enlace para activar tu cuenta:

    {url_for('auth.active_account', token=token, _external=True)}

    Si no solicitaste este restablecimiento de contraseña, simplemente ignora este correo electrónico.

    Gracias,

    Tu equipo de soporte.
        
    """
    
    msg = Message(subject, sender=sender_email, recipients=[recipient_email])
    msg.body = message_body
    mail.send(msg)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)  