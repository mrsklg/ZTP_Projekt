import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.user import User

def test_user_init():
    user = User(id=123, email="test@example.com", name="Jan", surname="Kowalski")
    assert user.id == "123"        
    assert user.email == "test@example.com"
    assert user.name == "Jan"
    assert user.surname == "Kowalski"


# test istniejący user
@patch('models.user.get_db_connection')
def test_user_get_existing_user(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "email@example.com", "Jan", "Kowalski")

    user = User.get(1)

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, email, name, surname FROM users WHERE id = %s", (1,)
    )
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    assert user is not None
    assert user.id == "1"
    assert user.email == "email@example.com"
    assert user.name == "Jan"
    assert user.surname == "Kowalski"


# test nieistniejący user
@patch('models.user.get_db_connection')
def test_user_get_not_existing_user(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    user = User.get(9999)

    assert user is None
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
