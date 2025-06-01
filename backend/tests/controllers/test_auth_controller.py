import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from controllers.auth_controller import auth_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'testkey'
    app.register_blueprint(auth_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()


# test login success
@patch('controllers.auth_controller.get_db_connection')
@patch('controllers.auth_controller.login_user')
def test_login_success(mock_login_user, mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    hashed = generate_password_hash('password123')
    mock_cursor.fetchone.return_value = (1, 'user@example.com', hashed, 'Jan', 'Kowalski')

    response = client.post('/login', json={'email': 'user@example.com', 'password': 'password123'})

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['email'] == 'user@example.com'
    mock_login_user.assert_called_once()


# test login brak danych
def test_login_missing_fields(client):
    response = client.post('/login', json={'email': 'user@example.com'})
    assert response.status_code == 400
    assert "wymagane" in response.get_json()['error'].lower()


# test login nieprawidłowe hasło
@patch('controllers.auth_controller.get_db_connection')
def test_login_bad_password(mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    hashed = generate_password_hash('correctpassword')
    mock_cursor.fetchone.return_value = (1, 'user@example.com', hashed, 'Jan', 'Kowalski')

    response = client.post('/login', json={'email': 'user@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert "nieprawidłowy" in response.get_json()['error'].lower()


# test rejestracja success
@patch('controllers.auth_controller.get_db_connection')
def test_register_success(mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.side_effect = [None,(1, 'user@example.com', datetime(2025, 1, 1, 0, 0, 0))]

    response = client.post('/register', json={
        'email': 'user@example.com',
        'password': 'pass123',
        'name': 'Jan',
        'surname': 'Kowalski'
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['email'] == 'user@example.com'


# test rejestracja - użytkownik juz istnieje
@patch('controllers.auth_controller.get_db_connection')
def test_register_user_exists(mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = (1,)

    response = client.post('/register', json={
        'email': 'user@example.com',
        'password': 'pass123',
    })
    assert response.status_code == 400
    assert "istnieje" in response.get_json()['error'].lower()


# test logout
@patch('controllers.auth_controller.logout_user')
@patch('flask_login.utils._get_user')
def test_logout(mock_get_user, mock_logout_user, client):
    mock_get_user.return_value.is_authenticated = True
    response = client.post('/logout')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "Wylogowano" in json_data['message']
    mock_logout_user.assert_called_once()


# test check_session - zalogowany
@patch('controllers.auth_controller.current_user')
def test_check_session_logged_in(mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_current_user.id = 123
    response = client.get('/session')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['logged_in'] is True
    assert json_data['user_id'] == 123


# test check_session - niezalogowany
@patch('controllers.auth_controller.current_user')
def test_check_session_logged_out(mock_current_user, client):
    mock_current_user.is_authenticated = False
    response = client.get('/session')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['logged_in'] is False


# test get_users success
@patch('controllers.auth_controller.get_db_connection')
def test_get_users_success(mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    from datetime import datetime
    mock_cursor.fetchall.return_value = [
        (1, 'user1@example.com', datetime(2025,5,28,12,34,56,789000)),
        (2, 'user2@example.com', datetime(2025,5,29,8,0,0,0)),
    ]

    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['email'] == 'user1@example.com'
