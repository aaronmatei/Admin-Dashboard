# third-party imports

from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
import datetime
from flask import Flask, redirect, render_template, url_for, render_template_string, request, flash, session
from flask_admin import Admin, BaseView, expose
from flask_mongoengine import MongoEngine
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_mongoengine import BaseQuerySet
from flask_user import login_required, UserManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeSerializer
from flask_mail import Mail, Message

# local imports
# from config import app_config


db = MongoEngine()
bcrypt = Bcrypt()
jwt = JWTManager()
CORS()
# user_manager = UserManager(app, db, User)
mail = Mail()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object(app_config[config_name])
    app.config.from_object(config_name)
    # app.config.from_pyfile('config.py')

    Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    login_manager.init_app(app)

    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
