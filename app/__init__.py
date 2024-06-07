from flask import Flask, request
from flask_login import LoginManager
from .config import Database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from flask_assets import Environment
from .assets import bundles
from flask_socketio import SocketIO
import os

load_dotenv()

loginManager = LoginManager()
db = SQLAlchemy()
dbConfig = Database()
migrate = Migrate()
assets = Environment()
mail = Mail()
io = SocketIO()

def create_app(): 
    app = Flask(__name__)
    
    assets = Environment(app)
    assets.debug = True
    assets.register(bundles)
    
    connectionParams = dbConfig.connString
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % connectionParams
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['PICTURES_FOLDER'] = os.path.join(app.root_path, 'static/img/profile/').replace("\\", "/")

    loginManager.login_view = "auth.auth"
    loginManager.init_app(app)

    db.init_app(app)   
    migrate.init_app(app, db)
    
    mail = configure_mail(app)

    from .auth import bp_auth
    app.register_blueprint(bp_auth)
    from .settings import bp_settings
    app.register_blueprint(bp_settings)
    from .chat import bp_chat
    app.register_blueprint(bp_chat)
    
    return app

def configure_mail(app: Flask):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] =  os.getenv("MAIL_PASSWORD")

    mail = Mail(app)
    return mail

app = create_app()
io = SocketIO(app, async_mode='threading', cors_allowed_origins="*")
users = {}

@io.on('connect')
def user_connects():
        print('User connected: ', request.sid)
        
@io.on('message')
def handle_message(message):
    print(message)
    io.emit('get-message', message, include_self=False)

@io.on('disconect')
def disconect():
    print('Un usuario se ha desconectado')