from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection

user_bp = Blueprint('user', __name__)

# zmiana hasła
@user_bp.route('/user/change-password', methods=['POST'])
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
@user_bp.route('/user/delete', methods=['DELETE'])
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

# pobieranie danych zalogowanego użytkownika
@user_bp.route('/me', methods=['GET'])
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

