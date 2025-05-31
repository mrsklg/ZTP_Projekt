from flask import Blueprint, jsonify
from utils.db import get_db_connection

db_bp = Blueprint('db', __name__)

# test bazy
@db_bp.route('/db-check')
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