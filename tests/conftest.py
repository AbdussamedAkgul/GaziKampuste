import pytest
from app import create_app, db
from app.models import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'

@pytest.fixture
def app():
    """Uygulamayı test konfigürasyonu ile oluşturur."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test istemcisini (client) döndürür."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI komutları için test koşucusunu döndürür."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Her testten önce veritabanını ilklendirir ve örnek bir kullanıcı oluşturur."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('TestPass123')
        db.session.add(user)
        db.session.commit()
        yield db
