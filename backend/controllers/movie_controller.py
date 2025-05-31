from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db_connection

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/watchlist', methods=['GET', 'POST', 'DELETE'])
@login_required
def watchlist():
    """
    Obsługuje operacje na watchliście (lista obejrzanych filmów).

    - GET: Zwraca listę filmów z watchlisty zalogowanego użytkownika.
      Przykład odpowiedzi:
        {
            "watchlist": ["tt1234567", "tt7654321"]
        }
      Kody odpowiedzi:
        200 - OK
        401 - Nie jesteś zalogowany
        500 - Błąd serwera

    - POST: Dodaje film do watchlisty.
      Wymagane dane w JSON:
        {
            "imdbID": "tt1234567"
        }
      Przykład odpowiedzi (201):
        {
            "id": "1",
            "movie_id": "tt1234567",
            "user_id": "42",
            "watched_at": "2025-06-01T15:30:00Z"
        }
      Kody odpowiedzi:
        201 - Dodano film
        400 - Film już istnieje / Brak imdbID
        500 - Błąd serwera

    - DELETE: Usuwa film z watchlisty.
      Wymagane dane w JSON:
        {
            "imdbID": "tt1234567"
        }
      Przykład odpowiedzi:
        {
            "message": "Film usunięty z watchlisty"
        }
      Kody odpowiedzi:
        200 - Usunięto film
        400 - Brak imdbID
        404 - Film nie znaleziony
        500 - Błąd serwera
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if request.method == 'GET':
            cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (current_user.id,))
            movies = [str(row[0]) for row in cur.fetchall()]
            cur.close()
            conn.close()
            return jsonify({"watchlist": movies}), 200

        data = request.get_json()
        movie_id = data.get('imdbID')
        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        if request.method == 'POST':
            cur.execute("SELECT id FROM watchlist WHERE user_id = %s AND movie_id = %s", (current_user.id, movie_id))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": "Film jest już w watchliście"}), 400

            cur.execute("INSERT INTO watchlist (user_id, movie_id) VALUES (%s, %s) RETURNING id, watched_at", (current_user.id, movie_id))
            new_entry = cur.fetchone()
            cur.execute("DELETE FROM wishlist WHERE user_id = %s AND movie_id = %s", (current_user.id, movie_id))
            conn.commit()

            cur.close()
            conn.close()

            remove_from_wishlist_internal(current_user.id, movie_id)


            return jsonify({"id": str(new_entry[0]), "movie_id": movie_id, "user_id": current_user.id, "watched_at": new_entry[1].isoformat()}), 201

        if request.method == 'DELETE':
            cur.execute("DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s RETURNING id", (current_user.id, movie_id))
            deleted = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if deleted:
                return jsonify({"message": "Film usunięty z watchlisty"}), 200
            else:
                return jsonify({"error": "Film nie znaleziony w watchliście"}), 404
        return None

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movie_bp.route('/wishlist', methods=['GET', 'POST', 'DELETE'])
@login_required
def wishlist():
    """
    Obsługuje operacje na wishliście (lista filmów do obejrzenia).

    - GET: Zwraca listę filmów z wishlisty.
      Przykład odpowiedzi:
        {
            "wishlist": ["tt1234567", "tt7654321"]
        }
      Kody odpowiedzi:
        200 - OK
        401 - Nie jesteś zalogowany
        500 - Błąd serwera

    - POST: Dodaje film do wishlisty.
      Wymagane dane w JSON:
        {
            "imdbID": "tt1234567"
        }
      Przykład odpowiedzi (201):
        {
            "id": "1",
            "movie_id": "tt1234567",
            "user_id": "42",
            "added_at": "2025-06-01T15:30:00Z"
        }
      Kody odpowiedzi:
        201 - Dodano film
        400 - Film już istnieje / Brak imdbID
        500 - Błąd serwera

    - DELETE: Usuwa film z wishlisty.
      Wymagane dane w JSON:
        {
            "imdbID": "tt1234567"
        }
      Przykład odpowiedzi:
        {
            "message": "Film usunięty z wishlisty"
        }
      Kody odpowiedzi:
        200 - Usunięto film
        400 - Brak imdbID
        404 - Film nie znaleziony
        500 - Błąd serwera
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if request.method == 'GET':
            cur.execute("SELECT movie_id FROM wishlist WHERE user_id = %s", (current_user.id,))
            movies = [str(row[0]) for row in cur.fetchall()]
            cur.close()
            conn.close()
            return jsonify({"wishlist": movies}), 200

        data = request.get_json()
        movie_id = data.get('imdbID')
        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        if request.method == 'POST':
            cur.execute("SELECT id FROM wishlist WHERE user_id = %s AND movie_id = %s", (current_user.id, movie_id))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": "Film jest już na wishliście"}), 400

            cur.execute("SELECT id FROM watchlist WHERE user_id = %s AND movie_id = %s", (current_user.id, movie_id))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": "Film jest już oznaczony jako obejrzany"}), 400

            cur.execute("INSERT INTO wishlist (user_id, movie_id) VALUES (%s, %s) RETURNING id, added_at", (current_user.id, movie_id))
            new_entry = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"id": str(new_entry[0]), "movie_id": movie_id, "user_id": current_user.id, "added_at": new_entry[1].isoformat()}), 201

        if request.method == 'DELETE':
            cur.execute("DELETE FROM wishlist WHERE user_id = %s AND movie_id = %s RETURNING id", (current_user.id, movie_id))
            deleted = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if deleted:
                return jsonify({"message": "Film usunięty z wishlisty"}), 200
            else:
                return jsonify({"error": "Film nie znaleziony w wishliście"}), 404
        return None

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movie_bp.route('/movies/likes', methods=['GET'])
@movie_bp.route('/movies/likes/<movie_id>', methods=['POST', 'DELETE'])
@login_required
def likes(movie_id=None):
    """
    Obsługuje operacje na polubieniach filmów.

    - GET: Zwraca listę polubionych filmów.
      Przykład odpowiedzi:
        {
            "likes": ["tt1234567", "tt7654321"]
        }
      Kody odpowiedzi:
        200 - OK
        401 - Nie jesteś zalogowany
        500 - Błąd serwera

    - POST: Dodaje film do polubionych.
      Wymagany parametr w ścieżce: movie_id (np. /movies/likes/tt1234567)
      Przykład odpowiedzi (201):
        {
            "id": "1",
            "movie_id": "tt1234567",
            "user_id": "42",
            "created_at": "2025-06-01T15:30:00Z"
        }
      Kody odpowiedzi:
        201 - Dodano film
        400 - Film już istnieje / Brak movie_id
        500 - Błąd serwera

    - DELETE: Usuwa film z polubionych.
      Wymagany parametr w ścieżce: movie_id (np. /movies/likes/tt1234567)
      Przykład odpowiedzi:
        {
            "message": "Film usunięty z likes"
        }
      Kody odpowiedzi:
        200 - Usunięto film
        400 - Brak movie_id
        404 - Film nie znaleziony
        500 - Błąd serwera
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if request.method == 'GET':
            cur.execute("SELECT movie_id FROM likes WHERE user_id = %s", (current_user.id,))
            movies = [str(row[0]) for row in cur.fetchall()]
            cur.close()
            conn.close()
            return jsonify({"likes": movies}), 200

        if not movie_id:
            return jsonify({"error": "Brak wymaganego parametru movie_id"}), 400

        if request.method == 'POST':
            cur.execute("SELECT id FROM likes WHERE user_id = %s AND movie_id = %s", (current_user.id, movie_id))
            if cur.fetchone():
                cur.close()
                conn.close()
                return jsonify({"error": "Film jest już w likes"}), 400

            cur.execute("INSERT INTO likes (user_id, movie_id) VALUES (%s, %s) RETURNING id, created_at", (current_user.id, movie_id))
            new_entry = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"id": str(new_entry[0]), "movie_id": movie_id, "user_id": current_user.id, "created_at": new_entry[1].isoformat()}), 201

        if request.method == 'DELETE':
            cur.execute("DELETE FROM likes WHERE user_id = %s AND movie_id = %s RETURNING id", (current_user.id, movie_id))
            deleted = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if deleted:
                return jsonify({"message": "Film usunięty z likes"}), 200
            else:
                return jsonify({"error": "Film nie znaleziony w likes"}), 404
        return None

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