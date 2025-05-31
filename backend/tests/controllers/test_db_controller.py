import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os

from controllers.db_controller import db_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(db_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()


# test połączenie z bazą - success
@patch('controllers.db_controller.get_db_connection')
def test_db_check_success(mock_get_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ("PostgreSQL 15.2 on x86_64-pc-linux-gnu",)

    response = client.get('/db-check')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert isinstance(data['version'], tuple) or isinstance(data['version'], list)
    assert "PostgreSQL" in data['version'][0]


# test połączenie z bazą - failure
@patch('controllers.db_controller.get_db_connection')
def test_db_check_failure(mock_get_db, client):
    mock_get_db.side_effect = Exception("Błąd połączenia z bazą danych")

    response = client.get('/db-check')
    assert response.status_code == 500
    data = response.get_json()
    assert data['status'] == 'error'
    assert "Błąd połączenia" in data['message']
