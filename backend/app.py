from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import psycopg2
from flasgger import Swagger

# Konfiguracja aplikacji
app = Flask(__name__)
app.secret_key = 'bardzo_tajne_haslo'
app.permanent_session_lifetime = timedelta(days=7)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3001", "http://127.0.0.1:3001"]}}, supports_credentials=True)

swagger = Swagger(app)

# Konfiguracja Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Funkcja połączenia z bazą danych
def get_db_connection():
    return psycopg2.connect(
        host='db',
        port=5432,
        database='mydatabase',
        user='myuser',
        password='mypassword'
    )

# Model użytkownika
class User(UserMixin):
    def __init__(self, id, email, name=None, surname=None):
        self.id = str(id)
        self.email = email
        self.name = name
        self.surname = surname

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, name, surname FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return User(*user)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')

    if not email or not password:
        return jsonify({"error": "Email i hasło są wymagane"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"error": "Użytkownik o takim email już istnieje"}), 400

        cur.execute(
            "INSERT INTO users (email, password, name, surname) VALUES (%s, %s, %s, %s) RETURNING id, email, created_at",
            (email, hashed_password, name, surname)
        )
        new_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": str(new_user[0]),
            "email": new_user[1],
            "created_at": new_user[2].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email i hasło są wymagane"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, email, password, name, surname FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user is None or not check_password_hash(user[2], password):
            return jsonify({"error": "Nieprawidłowy email lub hasło"}), 401

        user_obj = User(user[0], user[1], user[3], user[4])
        login_user(user_obj)

        return jsonify({
            "id": str(user[0]),
            "email": user[1]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Wylogowano"}), 200

@app.route('/api/session', methods=['GET'])
def check_session():
    if current_user.is_authenticated:
        return jsonify({"logged_in": True, "user_id": current_user.id})
    else:
        return jsonify({"logged_in": False}), 200

@app.route('/api/user/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    old_pwd = data.get('old_password')
    new_pwd = data.get('new_password')

    if not old_pwd or not new_pwd:
        return jsonify({"error": "Brak wymaganych danych"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT password FROM users WHERE id = %s", (current_user.id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Użytkownik nie istnieje"}), 404

        if not check_password_hash(row[0], old_pwd):
            return jsonify({"error": "Nieprawidłowe stare hasło"}), 400

        if check_password_hash(row[0], new_pwd):
            return jsonify({"error": "Nowe hasło nie może być takie samo jak stare"}), 400

        new_hashed_pwd = generate_password_hash(new_pwd)
        cur.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed_pwd, current_user.id))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Hasło zostało zmienione pomyślnie"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
