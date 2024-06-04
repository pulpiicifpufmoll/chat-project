import hashlib
from datetime import datetime
from flask import url_for
from sqlalchemy.orm import Mapped
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db
from app import loginManager

class User(db.Model, UserMixin):

    __tablename__ = "user"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname: Mapped[str] = db.Column(db.String(100), nullable=False)
    email: Mapped[str] = db.Column(db.String(50), unique=True, nullable=False)
    password:  Mapped[str] = db.Column(db.String(255), nullable=False)
    create_date: Mapped[datetime] = db.Column(db.DateTime,  default=datetime.now())
    role: Mapped[str] = db.Column(db.String(5))
    authenticated: Mapped[bool] = db.Column(db.Boolean, default=False, nullable=False)
    active: Mapped[bool] = db.Column(db.Boolean, default=False, nullable=False)
    profile_picture: Mapped[str] = db.Column(db.String(255))
    
    def __init__(self, fullname, email, password, create_date, role):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.create_date = create_date
        self.role = role
        self.authenticated = False
        self.active = False
        self.profile_picture = None
        
    def __repr__(self):
        return f'User {self.email}, {self.fullname}, created on: {self.create_date}, authenticated: {self.authenticated}'

    # --- SESSION --- #
    
    @loginManager.user_loader
    def load_user(id):
        user = User.get_user(id)
        if user is not None and user.is_authenticated():
            return user
        return None

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.role
    
    def is_authenticated(self):
        return self.authenticated
    
    def toJson(self):
        usuario_dict = {
            'fullname': self.fullname,
            'email': self.email,
            'role': self.role
        }
        return usuario_dict
 
    # --- REPO --- #
   
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self
    
    def active_user(self):
        self.update(active=True)
        
    @staticmethod
    def get_user(id):
        return User.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def hash_password(password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_password
    
    @staticmethod
    def check_password(hashed_password, password):
        # Verifica si el hash de la pass coincide con el hash proporcionado
        hashed_input_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed_input_password == hashed_password
