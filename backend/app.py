from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger


def get_db_connection():
    return psycopg2.connect(
        host='db',
        port=5432,
        database='mydatabase',
        user='myuser',
        password='mypassword'
    )


app = Flask(__name__)
app.secret_key = 'bardzo_tajne_haslo'
app.permanent_session_lifetime = timedelta(days=7)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3001", "http://127.0.0.1:3001"]}},
     supports_credentials=True)

swagger = Swagger(app)  # http://localhost:5000/apidocs/

# Konfiguracja Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

# zmiana hasła
@app.route('/api/user/change-password', methods=['POST'])
@login_required
def change_password():
    """
    Zmiana hasła użytkownika
    ---
    tags:
      - Użytkownicy
    security:
      - cookieAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - old_password
            - new_password
          properties:
            old_password:
              type: string
              example: stareHaslo123
              description: Stare hasło użytkownika
            new_password:
              type: string
              example: noweBezpieczneHaslo456
              description: Nowe hasło użytkownika
    responses:
      200:
        description: Hasło zostało pomyślnie zmienione
        schema:
          type: object
          properties:
            message:
              type: string
              example: Hasło zostało zmienione pomyślnie
      400:
        description: Nieprawidłowe dane wejściowe lub nieprawidłowe stare hasło
        schema:
          type: object
          properties:
            error:
              type: string
              example: Nieprawidłowe stare hasło
      401:
        description: Nieautoryzowany dostęp – użytkownik nie jest zalogowany
        schema:
          type: object
          properties:
            error:
              type: string
              example: Nieautoryzowany dostęp
      404:
        description: Użytkownik nie istnieje
        schema:
          type: object
          properties:
            error:
              type: string
              example: Użytkownik nie istnieje
      500:
        description: Błąd serwera
        schema:
          type: object
          properties:
            error:
              type: string
    """

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


# usuwanie konta
@app.route('/api/user/delete', methods=['DELETE'])
@login_required
def delete_account():
    """
    Usuwanie konta użytkownika
    ---
    tags:
      - Użytkownicy
    security:
      - cookieAuth: []
    responses:
      200:
        description: Konto zostało pomyślnie usunięte
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Konto zostało usunięte
      401:
        description: Nieautoryzowany dostęp – użytkownik nie jest zalogowany
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Nieautoryzowany dostęp
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
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (current_user.id,))
        conn.commit()
        cur.close()
        conn.close()
        logout_user()
        return jsonify({"message": "Konto zostało usunięte"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# rejestracja
@app.route('/api/register', methods=['POST'])
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


# logowanie
@app.route('/api/login', methods=['POST'])
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
              example: mocneHaslo123!
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


# sprawdzanie sesji
@app.route('/api/session', methods=['GET'])
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


# wylogowanie
@app.route('/api/logout', methods=['POST'])
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


# pobieranie danych zalogowanego użytkownika
@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Pobierz dane aktualnie zalogowanego użytkownika
    ---
    tags:
      - Użytkownicy
    security:
      - cookieAuth: []
    responses:
      200:
        description: Dane użytkownika
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                  format: uuid
                  example: "550e8400-e29b-41d4-a716-446655440000"
                email:
                  type: string
                  format: email
                  example: "jan.kowalski@example.com"
                name:
                  type: string
                  example: "Jan"
                surname:
                  type: string
                  example: "Kowalski"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-05-28T12:34:56.789Z"
                last_login:
                  type: string
                  format: date-time
                  example: "2025-05-30T08:15:42.123Z"
                is_active:
                  type: boolean
                  example: true
      401:
        description: Nieautoryzowany dostęp
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Wymagane uwierzytelnienie"
                code:
                  type: string
                  example: "UNAUTHORIZED"
      403:
        description: Brak uprawnień
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Brak wymaganych uprawnień"
                code:
                  type: string
                  example: "FORBIDDEN"
      404:
        description: Nie znaleziono zasobu
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Użytkownik nie istnieje"
                code:
                  type: string
                  example: "USER_NOT_FOUND"
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
                code:
                  type: string
                  example: "INTERNAL_SERVER_ERROR"
                request_id:
                  type: string
                  example: "req_123456789"
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, name, surname, created_at FROM users WHERE id = %s", (current_user.id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return jsonify({"id": str(user[0]), "email": user[1], "name": user[2], "surname": user[3],
                            "created_at": user[4].isoformat()}), 200
        else:
            return jsonify({'error': 'Użytkownik nie istnieje'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# użytkownicy
@app.route('/api/users', methods=['GET'])
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


# test bazy
@app.route('/api/db-check')
def db_check():
    """
    Sprawdzenie stanu bazy danych i wersji
    ---
    tags:
      - Diagnostyka
    responses:
      200:
        description: Połączenie z bazą danych jest OK, zwraca wersję bazy
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "ok"
                version:
                  type: array
                  items:
                    type: string
                  example: ["PostgreSQL 15.2 on x86_64-pc-linux-gnu"]
      500:
        description: Błąd połączenia z bazą danych
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "error"
                message:
                  type: string
                  example: "Błąd połączenia z bazą danych"
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"status": "ok", "version": version})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# pobieranie listy oglądniętych filmów
@app.route('/api/watchlist', methods=['GET'])
@login_required
def get_watchlist():
    """
    Pobierz listę filmów z watchlisty zalogowanego użytkownika
    ---
    tags:
      - Filmy
    responses:
      200:
        description: Lista filmów z watchlisty użytkownika
        content:
          application/json:
            schema:
              type: object
              properties:
                watchlist:
                  type: array
                  items:
                    type: string
                  example: ["123", "456", "789"]
      401:
        description: Użytkownik niezalogowany
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
                  example: "Błąd serwera"
    """

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (current_user.id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        movie_ids = [str(row[0]) for row in rows]
        return jsonify({"watchlist": movie_ids}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# pobranie listy filmów do oglądnięcia
@app.route('/api/wishlist', methods=['GET'])
@login_required
def get_wishlist():
    """
    Pobierz listę filmów z wishlisty użytkownika
    ---
    tags:
      - Filmy
    responses:
      200:
        description: Lista filmów z wishlisty użytkownika
        content:
          application/json:
            schema:
              type: object
              properties:
                wishlist:
                  type: array
                  items:
                    type: string
                  example: ["123", "456", "789"]
      401:
        description: Użytkownik niezalogowany
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
                  example: "Błąd serwera"
    """

     
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM wishlist WHERE user_id = %s", (current_user.id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        movie_ids = [str(row[0]) for row in rows]
        return jsonify({"wishlist": movie_ids}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# dodanie filmu do listy do oglądnięcia
@app.route('/api/wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    """
    Dodaj film do wishlisty użytkownika
    ---
    tags:
      - Filmy
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            imdbID:
              type: string
              example: "tt1234567"
          required:
            - imdbID
    responses:
      201:
        description: Film został dodany do wishlisty
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "123"
                movie_id:
                  type: string
                  example: "456"
                user_id:
                  type: string
                  example: "789"
                added_at:
                  type: string
                  format: date-time
                  example: "2025-05-28T12:34:56.789Z"
      400:
        description: Nieprawidłowe żądanie
        content:
          application/json:
            schema:
              oneOf:
                - type: object
                  properties:
                    error:
                      type: string
                      example: "Film jest już na wishliście"
                - type: object
                  properties:
                    error:
                      type: string
                      example: "Brak wymaganego pola imdbID"
      401:
        description: Użytkownik niezalogowany
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
                  example: "Błąd serwera"
    """

    try:
        data = request.get_json()
        movie_id = data.get('imdbID')

        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM wishlist WHERE user_id = %s AND movie_id = %s",
            (current_user.id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już na wishliście"}), 400

        cur.execute(
            "SELECT id FROM watchlist WHERE user_id = %s AND movie_id = %s",
            (current_user.id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już oznaczony jako obejrzany"}), 400

        # Dodanie do wishlisty
        cur.execute(
            "INSERT INTO wishlist (user_id, movie_id) VALUES (%s, %s) RETURNING id, added_at",
            (current_user.id, movie_id)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": current_user.id,
            "added_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# pobranie listy ulubionych filmów
@app.route('/api/movies/likes', methods=['GET'])
@login_required
def get_liked_movies():
    """
    Pobierz listę filmów polubionych przez zalogowanego użytkownika
    ---
    tags:
      - Filmy
    responses:
      200:
        description: Lista ID filmów polubionych przez użytkownika
        content:
          application/json:
            schema:
              type: object
              properties:
                likes:
                  type: array
                  items:
                    type: string
                  example: ["123", "456", "789"]
      401:
        description: Użytkownik niezalogowany
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
                  example: "Błąd serwera"
    """

     
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM likes WHERE user_id = %s", (current_user.id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        movie_ids = [str(row[0]) for row in rows]
        return jsonify({"likes": movie_ids}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# usunięcie wskazanego filmu z listy ulubionych
@app.route('/api/movies/likes/<movie_id>', methods=['DELETE'])
@login_required
def remove_from_likes(movie_id):
    """
    Usuń film z polubionych użytkownika
    ---
    tags:
      - Filmy
    parameters:
      - name: movie_id
        in: path
        type: string
        required: true
        description: ID filmu do usunięcia z polubionych
    responses:
      200:
        description: Film został usunięty z polubionych
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Film usunięty z likes"
      401:
        description: Użytkownik niezalogowany
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Nie jesteś zalogowany"
      404:
        description: Film nie znaleziony w polubionych
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Film nie znaleziony w likes"
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Błąd serwera"
    """

     
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM likes WHERE user_id = %s AND movie_id = %s RETURNING id",
            (current_user.id, movie_id)
        )
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return jsonify({"message": "Film usunięty z likes"}), 200
        else:
            return jsonify({"error": "Film nie znaleziony w likes"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# dodanie filmu do listy ulubionych
@app.route('/api/movies/likes/<movie_id>', methods=['POST'])
@login_required
def add_to_likes(movie_id):
    """
    Dodaj film do polubionych użytkownika
    ---
    tags:
      - Filmy
    parameters:
      - name: movie_id
        in: path
        type: string
        required: true
        description: ID filmu do dodania do polubionych
    responses:
      201:
        description: Film został dodany do polubionych
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "123"
                movie_id:
                  type: string
                  example: "456"
                user_id:
                  type: string
                  example: "789"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-05-28T12:34:56.789Z"
      400:
        description: Film jest już w polubionych
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Film jest już w likes"
      401:
        description: Użytkownik niezalogowany
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
                  example: "Błąd serwera"
    """

     
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Sprawdź czy już jest taki rekord (unikalność)
        cur.execute(
            "SELECT id FROM likes WHERE user_id = %s AND movie_id = %s",
            (current_user.id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już w likes"}), 400

        cur.execute(
            "INSERT INTO likes (user_id, movie_id) VALUES (%s, %s) RETURNING id, created_at",
            (current_user.id, movie_id)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": current_user.id,
            "created_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# usunięcie wskazanego filmu z listy do oglądnięcia
@app.route('/api/wishlist', methods=['DELETE'])
@login_required
def remove_from_wishlist():
    """
    Usuń film z wishlisty użytkownika
    ---
    tags:
      - Filmy
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            imdbID:
              type: string
              example: "tt1234567"
          required:
            - imdbID
    responses:
      200:
        description: Film został usunięty z wishlisty
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Film usunięty z wishlisty"
      400:
        description: Nieprawidłowe żądanie
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Brak wymaganego pola imdbID"
      401:
        description: Użytkownik niezalogowany
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Nie jesteś zalogowany"
      404:
        description: Film nie znaleziony na wishliście
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Film nie znaleziony na wishliście"
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Błąd serwera"
    """

    try:
        data = request.get_json()
        movie_id = data.get('imdbID')

        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM wishlist WHERE user_id = %s AND movie_id = %s RETURNING id",
            (current_user.id, movie_id)
        )
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return jsonify({"message": "Film usunięty z wishlisty"}), 200
        else:
            return jsonify({"error": "Film nie znaleziony w wishliście"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# usuwanie wybranego filmu z listy oglądniete
@app.route('/api/watchlist', methods=['DELETE'])
@login_required
def remove_from_watchlist():
    """
    Usuń film z watchlisty użytkownika
    ---
    tags:
      - Filmy
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            imdbID:
              type: string
              example: "tt1234567"
          required:
            - imdbID
    responses:
      200:
        description: Film został usunięty z watchlisty
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Film usunięty z watchlisty"
      400:
        description: Nieprawidłowe żądanie
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Brak wymaganego pola imdbID"
      401:
        description: Użytkownik niezalogowany
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Nie jesteś zalogowany"
      404:
        description: Film nie został znaleziony w watchliście
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Film nie znaleziony w watchliście"
      500:
        description: Błąd serwera
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Błąd serwera"
    """

    try:
        data = request.get_json()
        movie_id = data.get('imdbID')

        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s RETURNING id",
            (current_user.id, movie_id)
        )
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return jsonify({"message": "Film usunięty z watchlisty"}), 200
        else:
            return jsonify({"error": "Film nie znaleziony w watchliście"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# dodanie filmu do listy oglądnięte
@app.route('/api/watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    """
    Dodaj film do watchlisty użytkownika
    ---
    tags:
      - Filmy
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            imdbID:
              type: string
              example: "tt1234567"
          required:
            - imdbID
    responses:
      201:
        description: Film został dodany do watchlisty
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "123"
                movie_id:
                  type: string
                  example: "456"
                user_id:
                  type: string
                  example: "789"
                watched_at:
                  type: string
                  format: date-time
                  example: "2025-05-28T15:30:00"
      400:
        description: Nieprawidłowe żądanie
        content:
          application/json:
            schema:
              oneOf:
                - type: object
                  properties:
                    error:
                      type: string
                      example: "Film jest już na watchliście"
                - type: object
                  properties:
                    error:
                      type: string
                      example: "Brak wymaganego pola imdbID"
      401:
        description: Użytkownik niezalogowany
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
                  example: "Błąd serwera"
    """

     
    try:
        data = request.get_json()
        movie_id = data.get('imdbID')

        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM watchlist WHERE user_id = %s AND movie_id = %s",
            (current_user.id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już w watchliście"}), 400

        cur.execute(
            "INSERT INTO watchlist (user_id, movie_id) VALUES (%s, %s) RETURNING id, watched_at",
            (current_user.id, movie_id)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        remove_from_wishlist_internal(current_user.id, movie_id)

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": current_user.id,
            "watched_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def remove_from_wishlist_internal(user_id, movie_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM wishlist WHERE user_id = %s AND movie_id = %s RETURNING id",
            (user_id, movie_id)
        )
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return deleted is not None

    except Exception as e:
        print(f"Błąd usuwania z wishlisty: {e}")
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)