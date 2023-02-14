from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import urandom


app = Flask(__name__)

admins = (
        'admin1',
        'admin2'
)

with app.app_context():
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sec_san.db'
    app.config['WTF_CSRF_SECRET_KEY'] = urandom(12).hex()
    db = SQLAlchemy(app)

    app.secret_key = urandom(12).hex()

    import myapp.routes, myapp.models

    db.create_all()
