from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager
from flasgger import Swagger
from datetime import timedelta
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.movie_controller import movie_bp
from controllers.db_controller import db_bp
from models.user import User

app = Flask(__name__)
app.secret_key = 'bardzo_tajne_haslo'
app.permanent_session_lifetime = timedelta(days=7)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3001", "http://127.0.0.1:3001"]}},
     supports_credentials=True)

swagger = Swagger(app)  # http://localhost:5000/apidocs/

# Konfiguracja Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(movie_bp, url_prefix='/api')
app.register_blueprint(db_bp, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)