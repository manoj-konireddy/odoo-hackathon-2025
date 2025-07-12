from flask import Blueprint, request
from app import mysql, bcrypt
from app.utils import response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, hashed_pw))
        mysql.connection.commit()
        cur.close()

        return response(message="User registered successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("🔥 Registration error:", e)
        return response(success=False, message=f"Registration failed: {str(e)}"), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user[1], password):
        return response(message="Login successful", data={"user_id": user[0]})
    return response(success=False, message="Invalid credentials")
