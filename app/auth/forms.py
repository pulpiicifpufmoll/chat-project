from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_login import current_user
from .models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Correo electrónico", "id": "email-log"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Contraseña", "id": "password-log"})
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión',  render_kw={"id": "submit-login"})
    form_key = HiddenField('form-key', default='')

    
class RegisterForm(FlaskForm):
    fullname = StringField('Nombre', validators=[DataRequired()], render_kw={"placeholder": "Nombre", "id": "fullname"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Correo electrónico", "id": "email-reg"})
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Contraseña", "id": "password-register"})
    password_confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired(), Length(min=8), EqualTo('password')], render_kw={"placeholder": "Confirmar contraseña", "id": "password-confirm-register"})
    submit = SubmitField('Crear cuenta', render_kw={"id": "submit-register"})
    form_key = HiddenField('form-key', default='')

class SettingsData(FlaskForm):
    fullname = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    form_key = HiddenField('form-key', default="form-main")

class SettingsPasswords(FlaskForm):
    old_password = PasswordField('Contraseña antigua', validators=[DataRequired()], render_kw={"id": "old-password"})
    new_password = PasswordField('Contraseña nueva', validators=[DataRequired(), Length(min=8)], render_kw={"id": "new_password"})
    repeat_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), Length(min=8), EqualTo('new_password', message='Las contraseñas deben coincidir')], render_kw={"id": "repeat-password"})
    form_key = HiddenField('form-key', default="form-password")
