from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from utils.db import get_db_connection

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/watchlist', methods=['GET'])
@login_required
def get_watchlist():
    """
    Pobierz listę filmów z watchlisty użytkownika
    ---
    tags:
      - Watchlist
    security:
      - cookieAuth: []
    responses:
      200:
        description: Zwrócono listę filmów
        schema:
          type: object
          properties:
            watchlist:
              type: array
              items:
                type: string
              example: ["tt1234567", "tt7654321"]
      401:
        description: Nieautoryzowany dostęp
      500:
        description: Błąd serwera
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM watchlist WHERE user_id = %s", (current_user.id,))
        movies = [str(row[0]) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify({"watchlist": movies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@movie_bp.route('/watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    """
    Dodaj film do watchlisty
    ---
    tags:
      - Watchlist
    security:
      - cookieAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - imdbID
          properties:
            imdbID:
              type: string
              example: tt1234567
    responses:
      201:
        description: Dodano film do watchlisty
        schema:
          type: object
          properties:
            id:
              type: string
            movie_id:
              type: string
            user_id:
              type: integer
            watched_at:
              type: string
              format: date-time
      400:
        description: Film już istnieje lub brak imdbID
      401:
        description: Nieautoryzowany dostęp
      500:
        description: Błąd serwera
    """
    try:
        data = request.get_json()
        movie_id = data.get('imdbID')
        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

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

        return jsonify({
            "id": str(new_entry[0]),
            "movie_id": movie_id,
            "user_id": current_user.id,
            "watched_at": new_entry[1].isoformat()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@movie_bp.route('/watchlist', methods=['DELETE'])
@login_required
def remove_from_watchlist():
    """
    Usuń film z watchlisty
    ---
    tags:
      - Watchlist
    security:
      - cookieAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - imdbID
          properties:
            imdbID:
              type: string
              example: tt1234567
    responses:
      200:
        description: Film usunięty z watchlisty
        schema:
          type: object
          properties:
            message:
              type: string
              example: Film usunięty z watchlisty
      400:
        description: Brak imdbID
      404:
        description: Film nie znaleziony w watchlisty
      401:
        description: Nieautoryzowany dostęp
      500:
        description: Błąd serwera
    """
    try:
        data = request.get_json()
        movie_id = data.get('imdbID')
        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s RETURNING id", (current_user.id, movie_id))
        deleted = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        if deleted:
            return jsonify({"message": "Film usunięty z watchlisty"}), 200
        else:
            return jsonify({"error": "Film nie znaleziony w watchlisty"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@movie_bp.route('/wishlist', methods=['GET'])
@login_required
def get_wishlist():
    """
    Pobierz listę filmów z wishlisty użytkownika
    ---
    tags:
      - Wishlist
    security:
      - cookieAuth: []
    responses:
      200:
        description: Lista filmów z wishlisty
        schema:
          type: object
          properties:
            wishlist:
              type: array
              items:
                type: string
              example: ["tt1234567", "tt7654321"]
      401:
        description: Użytkownik nie jest zalogowany
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Błąd serwera
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie_id FROM wishlist WHERE user_id = %s", (current_user.id,))
        movies = [str(row[0]) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify({"wishlist": movies}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@movie_bp.route('/wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    """
    Dodaje film do wishlisty.
    ---
    tags:
      - Wishlist
    security:
      - cookieAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - imdbID
          properties:
            imdbID:
              type: string
              example: tt1234567
              description: ID filmu z IMDb
    responses:
      201:
        description: Film dodany do wishlisty
        schema:
          type: object
          properties:
            id:
              type: string
            movie_id:
              type: string
            user_id:
              type: integer
            added_at:
              type: string
              format: date-time
      400:
        description: Błąd danych wejściowych lub film już istnieje
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Błąd serwera
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()
        movie_id = data.get('imdbID')
        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

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

        cur.execute("INSERT INTO wishlist (user_id, movie_id) VALUES (%s, %s) RETURNING id, added_at",
                    (current_user.id, movie_id))
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


@movie_bp.route('/wishlist', methods=['DELETE'])
@login_required
def remove_from_wishlist():
    """
    Usuwa film z wishlisty.
    ---
    tags:
      - Wishlist
    security:
      - cookieAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - imdbID
          properties:
            imdbID:
              type: string
              example: tt1234567
              description: ID filmu do usunięcia
    responses:
      200:
        description: Film usunięty z wishlisty
        schema:
          type: object
          properties:
            message:
              type: string
              example: Film usunięty z wishlisty
      400:
        description: Brak imdbID
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Film nie znaleziony
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Błąd serwera
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()
        movie_id = data.get('imdbID')
        if not movie_id:
            return jsonify({"error": "Brak wymaganego pola imdbID"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM wishlist WHERE user_id = %s AND movie_id = %s RETURNING id",
                    (current_user.id, movie_id))
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