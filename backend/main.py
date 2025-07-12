from routes.answers import answers_bp
from routes.questions import questions_bp
from routes.auth import auth_bp
from models.answer import Answer
from models.question import Question
from models.user import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# App configuration
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "stackit-default-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Import models

# Register routes (you’ll add actual route files soon)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(questions_bp, url_prefix="/api/questions")
app.register_blueprint(answers_bp, url_prefix="/api/answers")

# Start the server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if not exist
    app.run(debug=True)
