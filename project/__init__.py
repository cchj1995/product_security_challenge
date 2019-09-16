# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .users import User
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    
    app.debug = True;
    app.run(host = '0.0.0.0', port = 5000,ssl_context='adhoc');

    return app