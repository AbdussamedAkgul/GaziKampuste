from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
babel = Babel()

login.login_view = 'auth.login'
login.login_message = 'Bu sayfaya erişebilmek için lütfen giriş yapın.'
login.login_message_category = 'warning'

def get_locale():
    # Session'da kaydedilmiş bir dil varsa onu kullan
    if 'language' in session:
        return session['language']
    # Yoksa tarayıcı dillerinden desteklediğimizi seç
    return request.accept_languages.best_match(Config.LANGUAGES)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # Modellerin ve user_loader'ın yüklenmesi
    from app import models

    # Blueprint'lerin kaydedilmesi
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.api.v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
