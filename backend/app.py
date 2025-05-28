from flask import Flask, jsonify, request, session
from flask_cors import CORS
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
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3001"}}, supports_credentials=True)
swagger = Swagger(app)

# zmiana hasła
@app.route('/api/change_pswd', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({"error": "Nieautoryzowany dostęp"}), 401

    user_id = session['user_id']
    data = request.get_json()

    old_pwd = data.get('old_password')
    new_pwd = data.get('new_password')

    if not old_pwd or not new_pwd:
        return jsonify({"error": "Brak wymaganych danych"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Użytkownik nie istnieje"}), 404

        current_hashed_pwd = row[0]

        if not check_password_hash(current_hashed_pwd, old_pwd):
            return jsonify({"error": "Nieprawidłowe stare hasło"}), 400

        if check_password_hash(current_hashed_pwd, new_pwd):
            return jsonify({"error": "Nowe hasło nie może być takie samo jak stare"}), 400

        new_hashed_pwd = generate_password_hash(new_pwd)
        cur.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed_pwd, user_id))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Hasło zostało zmienione pomyślnie"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# usuwanie konta    
@app.route('/api/delete_account', methods=['DELETE'])
def delete_account():
    if 'user_id' not in session:
        return jsonify({"error": "Nieautoryzowany dostęp"}), 401

    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        cur.close()
        conn.close()

        session.clear()

        return jsonify({"message": "Konto zostało usunięte"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500    

# rejestracja
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')

    if not email or not password:
        return jsonify({"error": "Email i hasło są wymagane"}), 400

    hashed_password = generate_password_hash(password)  # hashowanie hasła

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
    
#logowanie    
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

        # Pobierz użytkownika
        cur.execute("SELECT id, email, password, created_at FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user is None:
            return jsonify({"error": "Nieprawidłowy email lub hasło"}), 401

        user_id, user_email, hashed_password, created_at = user

        if not check_password_hash(hashed_password, password):
            return jsonify({"error": "Nieprawidłowy email lub hasło"}), 401
        
        session.permanent = True
        session['user_id'] = str(user_id)

        return jsonify({
            "id": str(user_id),
            "email": user_email,
            "created_at": str(created_at)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# sprawdzanie sesji    
@app.route('/api/session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        return jsonify({"logged_in": True, "user_id": user_id})
    else:
        return jsonify({"logged_in": False}), 200
    
#wylogowanie    
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Wylogowano"}), 200

# pobieranie danych zalogowanego użytkownika
@app.route('/api/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Pobieramy wszystkie pola oprócz password
        cur.execute("SELECT id, email, name, surname, created_at FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify({
                "id": str(user[0]),
                "email": user[1],
                "name": user[2],
                "surname": user[3],
                "created_at": user[4].isoformat()
            }), 200
        else:
            return jsonify({"error": "Użytkownik nie istnieje"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# użytkownicy
@app.route('/api/users', methods=['GET'])
def get_users():
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

#test bazy
@app.route('/api/db-check')
def db_check():
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
@app.route('/api/movies/watched', methods=['GET'])
def get_watched_movies():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM watched WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        movie_ids = [str(row[0]) for row in rows]
        return jsonify({"watched": movie_ids}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# usuwanie wybranego filmu z listy oglądniete    
@app.route('/api/movies/watched/<movie_id>', methods=['DELETE'])
def remove_from_watched(movie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM watched WHERE user_id = %s AND movie_id = %s RETURNING id",
            (user_id, movie_id)
        )
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return jsonify({"message": "Film usunięty z watched"}), 200
        else:
            return jsonify({"error": "Film nie znaleziony w watched"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# dodanie filmu do listy oglądnięte
@app.route('/api/movies/watched/<movie_id>', methods=['POST'])
def add_to_watched(movie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM watched WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już w watched"}), 400

        cur.execute(
            "INSERT INTO watched (user_id, movie_id) VALUES (%s, %s) RETURNING id, watched_at",
            (user_id, movie_id)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        remove_from_watchlist(movie_id)

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": user_id,
            "watched_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# pobranie listy filmów do oglądnięcia
@app.route('/api/movies/watchlist', methods=['GET'])
def get_watchlist_movies():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        movie_ids = [str(row[0]) for row in rows]
        return jsonify({"watchlist": movie_ids}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# usunięcie wskazanego filmu z listy do oglądnięcia    
@app.route('/api/movies/watchlist/<movie_id>', methods=['DELETE'])
def remove_from_watchlist(movie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s RETURNING id",
            (user_id, movie_id)
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

# dodanie filmu do listy do oglądnięcia
@app.route('/api/movies/watchlist/<movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM watchlist WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już na watchliście"}), 400

        cur.execute(
            "SELECT id FROM watched WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już oznaczony jako obejrzany"}), 400

        # Dodanie do watchlisty
        cur.execute(
            "INSERT INTO watchlist (user_id, movie_id) VALUES (%s, %s) RETURNING id, added_at",
            (user_id, movie_id)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": user_id,
            "added_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# pobranie listy ulubionych filmów
@app.route('/api/movies/likes', methods=['GET'])
def get_liked_movies():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM likes WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        movie_ids = [str(row[0]) for row in rows]
        return jsonify({"likes": movie_ids}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# usunięcie wskazanego filmu z listy ulubionych    
@app.route('/api/movies/likes/<movie_id>', methods=['DELETE'])
def remove_from_likes(movie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM likes WHERE user_id = %s AND movie_id = %s RETURNING id",
            (user_id, movie_id)
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
def add_to_likes(movie_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Nie jesteś zalogowany"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Sprawdź czy już jest taki rekord (unikalność)
        cur.execute(
            "SELECT id FROM likes WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Film jest już w likes"}), 400

        cur.execute(
            "INSERT INTO likes (user_id, movie_id) VALUES (%s, %s) RETURNING id, created_at",
            (user_id, movie_id)
        )
        new_entry = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": user_id,
            "created_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)