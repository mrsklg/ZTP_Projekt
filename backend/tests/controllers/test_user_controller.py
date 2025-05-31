import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin

from controllers.user_controller import user_bp


class DummyUser(UserMixin):
    def __init__(self, id):
        self.id = id

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return DummyUser(user_id)

    app.register_blueprint(user_bp, url_prefix='/api')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def logged_in_client(app, client):
    with client.session_transaction() as sess:
        sess['_user_id'] = "42"
    yield client

# test zmiana hasła - success
def test_change_password_success(logged_in_client):
    with patch('controllers.user_controller.get_db_connection') as mock_db_conn, \
         patch('controllers.user_controller.check_password_hash') as mock_check_hash, \
         patch('controllers.user_controller.generate_password_hash') as mock_generate_hash:

        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("oldhashedpassword",)

        mock_check_hash.side_effect = lambda hash, pwd: (pwd == "oldpass")
        mock_generate_hash.return_value = "newhashedpassword"

        response = logged_in_client.post('/api/user/change-password', json={
            "old_password": "oldpass",
            "new_password": "newpass"
        })

        assert response.status_code == 200
        assert response.json == {"message": "Hasło zostało zmienione pomyślnie"}
        mock_cursor.execute.assert_any_call("UPDATE users SET password = %s WHERE id = %s",
                                            ("newhashedpassword", "42"))


# test zmiana hasła - złe stare hasło
def test_change_password_wrong_old_password(logged_in_client):
    with patch('controllers.user_controller.get_db_connection') as mock_db_conn, \
         patch('controllers.user_controller.check_password_hash') as mock_check_hash:

        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("oldhashedpassword",)
        mock_check_hash.side_effect = lambda hash, pwd: False

        response = logged_in_client.post('/api/user/change-password', json={
            "old_password": "wrongold",
            "new_password": "newpass"
        })

        assert response.status_code == 400
        assert response.json == {"error": "Nieprawidłowe stare hasło"}


# test zmiana hasła - brak danych
def test_change_password_no_data(logged_in_client):
    response = logged_in_client.post('/api/user/change-password', json={})
    assert response.status_code == 400
    assert "error" in response.json


# test usuwanie konta - success
def test_delete_account_success(logged_in_client):
    with patch('controllers.user_controller.get_db_connection') as mock_db_conn, \
         patch('controllers.user_controller.logout_user') as mock_logout_user:

        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor

        response = logged_in_client.delete('/api/user/delete')
        assert response.status_code == 200
        assert response.json == {"message": "Konto zostało usunięte"}
        mock_cursor.execute.assert_called_once_with("DELETE FROM users WHERE id = %s", ("42",))
        mock_logout_user.assert_called_once()


# test pobieranie danych zalogowanego użytkownika
def test_get_current_user_success(logged_in_client):
    with patch('controllers.user_controller.get_db_connection') as mock_db_conn:
        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor

        from datetime import datetime
        user_data = ("uuid-1234", "email@example.com", "Jan", "Kowalski", datetime(2025,5,28,12,34,56))
        mock_cursor.fetchone.return_value = user_data

        response = logged_in_client.get('/api/me')

        assert response.status_code == 200
        assert response.json == {
            "id": "uuid-1234",
            "email": "email@example.com",
            "name": "Jan",
            "surname": "Kowalski",
            "created_at": "2025-05-28T12:34:56"
        }


# test pobieranie danych zalogowanego użytkownika - nie istnieje
def test_get_current_user_not_found(logged_in_client):
    with patch('controllers.user_controller.get_db_connection') as mock_db_conn:
        mock_cursor = MagicMock()
        mock_db_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        response = logged_in_client.get('/api/me')
        assert response.status_code == 404
        assert response.json == {'error': 'Użytkownik nie istnieje'}
