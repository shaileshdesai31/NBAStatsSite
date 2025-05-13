from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_URI = "INSERT_DB_URI_HERE"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'special_NBA_key'
    # example URI on localhost: f"mysql+mysqlconnector://root:{DB_PWD}@127.0.0.1/{DB_NAME}"
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

    db.init_app(app)

    from viewsf import views
    from authf import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

