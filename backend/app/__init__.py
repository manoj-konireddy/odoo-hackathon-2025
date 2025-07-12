from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS

mysql = MySQL()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'stackit'

    mysql.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.questions import questions_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(questions_bp, url_prefix='/questions')

    return app
