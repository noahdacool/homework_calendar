from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('HOMEWORK_CALENDAR_SECRET_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HOMEWORK_CALENDAR_DATABASE_URL')
    db.init_app(app)

    from .views import views_blueprint
    from .auth import auth_blueprint

    app.register_blueprint(views_blueprint, url_prefix='/')
    app.register_blueprint(auth_blueprint, url_prefix='/')

    from .models import User, Category, Assignment

    login_manager = LoginManager()
    login_manager.login_view = 'auth_str.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app