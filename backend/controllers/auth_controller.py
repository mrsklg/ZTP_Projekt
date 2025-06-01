from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

# logowanie
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logowanie użytkownika
    ---
    tags:
      - Użytkownicy
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
              description: Adres email użytkownika
            password:
              type: string
              example: Haslo123!
              description: Hasło użytkownika
    responses:
      200:
        description: Pomyślne logowanie
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "507f1f77bcf86cd799439011"
                email:
                  type: string
                  example: user@example.com
                created_at:
                  type: string
                  format: date-time
                  example: "2023-01-01T00:00:00Z"
      400:
        description: Brak wymaganych danych
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Wymagane pola: email, password"
      401:
        description: Nieprawidłowy email lub hasło
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Nieprawidłowe dane logowania"
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Wewnętrzny błąd serwera"
    """

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

# rejestracja
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Rejestracja nowego użytkownika
    ---
    tags:
      - Użytkownicy
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
              description: Adres email użytkownika
            password:
              type: string
              example: Haslo123!
              description: Hasło użytkownika
            name:
              type: string
              example: Jan
              description: Imię użytkownika
            surname:
              type: string
              example: Kowalski
              description: Nazwisko użytkownika
    responses:
      201:
        description: Użytkownik został pomyślnie zarejestrowany
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                email:
                  type: string
                created_at:
                  type: string
      400:
        description: Nieprawidłowe dane wejściowe lub użytkownik już istnieje
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """

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

# wylogowanie
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Wylogowanie użytkownika (usunięcie sesji)
    ---
    tags:
      - Użytkownicy
    responses:
      200:
        description: Sukces wylogowania
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Wylogowano pomyślnie"
      401:
        description: Brak aktywnej sesji
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Nie jesteś zalogowany"
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Wewnętrzny błąd serwera"
    """

    logout_user()
    return jsonify({"message": "Wylogowano"}), 200

# sprawdzanie sesji
@auth_bp.route('/session', methods=['GET'])
def check_session():
    """
    Sprawdzenie sesji użytkownika
    ---
    tags:
      - Użytkownicy
    responses:
      200:
        description: Informacja o stanie sesji
        content:
          application/json:
            schema:
              oneOf:
                - type: object
                  properties:
                    logged_in:
                      type: boolean
                      example: true
                    user_id:
                      type: integer
                      example: 123
                - type: object
                  properties:
                    logged_in:
                      type: boolean
                      example: false
    """

    if current_user.is_authenticated:
        return jsonify({"logged_in": True, "user_id": current_user.id})
    else:
        return jsonify({"logged_in": False}), 200

# użytkownicy
@auth_bp.route('/users', methods=['GET'])
def get_users():
    """
    Pobierz listę wszystkich użytkowników
    ---
    tags:
      - Użytkownicy
    responses:
      200:
        description: Lista użytkowników
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "123"
                  email:
                    type: string
                    example: "user@example.com"
                  created_at:
                    type: string
                    format: date-time
                    example: "2025-05-28T12:34:56.789Z"
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Internal server error"
    """

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, created_at from users")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": str(row[0]),
            "email": row[1],
            "created_at": row[2].isoformat()
        })

    return jsonify(users)