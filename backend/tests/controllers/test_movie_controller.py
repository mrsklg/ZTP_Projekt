import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import LoginManager, UserMixin
from datetime import datetime

from controllers.movie_controller import movie_bp

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

    app.register_blueprint(movie_bp, url_prefix='/api')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def logged_in_client(app, client):
    with app.test_request_context():
        user = DummyUser("42")
        from flask_login import login_user
        login_user(user)
        with client.session_transaction() as sess:
            sess['_user_id'] = user.id
        yield client


# test pobranie watchlisty
@patch('controllers.movie_controller.get_db_connection')
def test_watchlist_get(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [('tt1234567',), ('tt7654321',)]

    response = logged_in_client.get('/api/watchlist')

    assert response.status_code == 200
    assert response.get_json() == {"watchlist": ["tt1234567", "tt7654321"]}
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# test dodanie do watchlisty - już istnieje
@patch('controllers.movie_controller.get_db_connection')
def test_watchlist_post_existing(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)

    response = logged_in_client.post('/api/watchlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Film jest już w watchliście"}


# test dodanie do watchlisty - success
@patch('controllers.movie_controller.get_db_connection')
@patch('controllers.movie_controller.remove_from_wishlist_internal')
def test_watchlist_post_add_new(mock_remove, mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [None, (1, datetime(2025, 6, 1, 15, 30, 0))]

    mock_remove.return_value = True

    response = logged_in_client.post('/api/watchlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == "1"
    assert data["movie_id"] == "tt1234567"
    assert data["user_id"] == "42"
    assert "watched_at" in data

    mock_conn.commit.assert_called_once()
    mock_remove.assert_called_once_with("42", "tt1234567")


# test usuwanie z watchlisty - brak id
@patch('controllers.movie_controller.get_db_connection')
def test_watchlist_delete_no_imdbID(mock_get_db_conn, logged_in_client):
    response = logged_in_client.delete('/api/watchlist', json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Brak wymaganego pola imdbID"}


# test usuwanie z watchlisty - success
@patch('controllers.movie_controller.get_db_connection')
def test_watchlist_delete_found(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)

    response = logged_in_client.delete('/api/watchlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 200
    assert response.get_json() == {"message": "Film usunięty z watchlisty"}


# test usuwanie w watchlisty - nie znaleziono
@patch('controllers.movie_controller.get_db_connection')
def test_watchlist_delete_not_found(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    response = logged_in_client.delete('/api/watchlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "Film nie znaleziony w watchliście"}


# test pobranie wishlisty
@patch('controllers.movie_controller.get_db_connection')
def test_wishlist_get(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [('tt1111111',), ('tt2222222',)]

    response = logged_in_client.get('/api/wishlist')

    assert response.status_code == 200
    assert response.get_json() == {"wishlist": ["tt1111111", "tt2222222"]}

# test dodanie do wishlisty - już istnieje
@patch('controllers.movie_controller.get_db_connection')
def test_wishlist_post_existing(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)

    response = logged_in_client.post('/api/wishlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Film jest już na wishliście"}


# test dodanie do wishlisty - success
@patch('controllers.movie_controller.get_db_connection')
def test_wishlist_post_add_new(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [None,None,(1, datetime(2025, 6, 1, 15, 30, 0))]

    response = logged_in_client.post('/api/wishlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == "1"
    assert data["movie_id"] == "tt1234567"
    assert str(data["user_id"]) == "42"
    assert "added_at" in data

    mock_conn.commit.assert_called_once()



# test usuwanie z wishlisty - brak id
@patch('controllers.movie_controller.get_db_connection')
def test_wishlist_delete_no_imdbID(mock_get_db_conn, logged_in_client):
    response = logged_in_client.delete('/api/wishlist', json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Brak wymaganego pola imdbID"}


# test usuwanie z wishlisty - success
@patch('controllers.movie_controller.get_db_connection')
def test_wishlist_delete_found(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)

    response = logged_in_client.delete('/api/wishlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 200
    assert response.get_json() == {"message": "Film usunięty z wishlisty"}


# test usuwanie z wishlisty - nie znaleziono
@patch('controllers.movie_controller.get_db_connection')
def test_wishlist_delete_not_found(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    response = logged_in_client.delete('/api/wishlist', json={"imdbID": "tt1234567"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "Film nie znaleziony w wishliście"}


# test pobieranie ulubionych
@patch('controllers.movie_controller.get_db_connection')
def test_likes_get(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [('tt3333333',), ('tt4444444',)]

    response = logged_in_client.get('/api/movies/likes')

    assert response.status_code == 200
    assert response.get_json() == {"likes": ["tt3333333", "tt4444444"]}


# test dodanie do ulubionych - już istnieje
@patch('controllers.movie_controller.get_db_connection')
def test_likes_post_already_exists(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)

    response = logged_in_client.post('/api/movies/likes/tt5555555')

    assert response.status_code == 400
    assert response.get_json() == {"error": "Film jest już w likes"}


# test dodanie do ulubionych - success
@patch('controllers.movie_controller.get_db_connection')
def test_likes_post_success(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [None, (1, datetime(2025, 6, 1, 15, 30, 0))]

    response = logged_in_client.post('/api/movies/likes/tt5555555')

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == "1"
    assert data["movie_id"] == "tt5555555"
    assert data["user_id"] == "42"
    assert "created_at" in data


# test usuwanie z ulubionych - success
@patch('controllers.movie_controller.get_db_connection')
def test_likes_delete_found(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)

    response = logged_in_client.delete('/api/movies/likes/tt5555555')

    assert response.status_code == 200
    assert response.get_json() == {"message": "Film usunięty z likes"}


# test usuwanie z ulubionych - nie znaleziono
@patch('controllers.movie_controller.get_db_connection')
def test_likes_delete_not_found(mock_get_db_conn, logged_in_client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    response = logged_in_client.delete('/api/movies/likes/tt5555555')

    assert response.status_code == 404
    assert response.get_json() == {"error": "Film nie znaleziony w likes"}
