from flask_login import UserMixin
from utils.db import get_db_connection

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