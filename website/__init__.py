from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'parola segreta segretissima'    
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:7yYzL~WJ?G2/RyP@16.16.127.54/flix"
    db.init_app(app)

    from .frontend import frontend
    from .auth import auth
    from .ajax import ajax
    from .management import management

    app.register_blueprint(frontend, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(management, url_prefix='/')
    app.register_blueprint(ajax, url_prefix='/ajax')

    from .models import Utente
    
    with app.app_context():
        db.create_all()
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Utente.query.get(int(id))
    return app
