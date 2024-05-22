from flask import Flask
from flask_login import LoginManager
from .config import Database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from flask_assets import Environment
from .assets import bundles
import os

load_dotenv()

loginManager = LoginManager()
db = SQLAlchemy()
dbConfig = Database()
migrate = Migrate()
assets = Environment()
mail = Mail()

def create_app(): 
    app = Flask(__name__)
    
    assets = Environment(app)
    assets.debug = app.debug
    assets.register(bundles)
    
    connectionParams = dbConfig.connString
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % connectionParams
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    
    loginManager.login_view = "auth.auth"
    loginManager.init_app(app)

    db.init_app(app)   
    migrate.init_app(app, db)
    
    mail = configure_mail(app)

    from .auth import bp_auth
    app.register_blueprint(bp_auth)
    from .admin import bp_admin
    app.register_blueprint(bp_admin)
    from .chat import bp_chat
    app.register_blueprint(bp_chat)
    from .error_handling import bp_errors
    app.register_blueprint(bp_errors)
    
    return app

def configure_mail(app: Flask):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "angel24.practicas@gmail.com"
    app.config['MAIL_PASSWORD'] = "gdzyqdqtsmmhwkye"

    mail = Mail(app)
    return mail
