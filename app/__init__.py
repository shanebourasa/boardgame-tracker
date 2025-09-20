from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()
bootstrap = Bootstrap5()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_urlsafe(16)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boardgames.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)

    # Import routes
    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
