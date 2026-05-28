import pytest
from app.models import User
from app import db

def test_successful_registration(client, app):
    """Geçerli bilgilerle yeni bir kullanıcı kaydının başarıyla gerçekleştiğini test eder."""
    response = client.post('/auth/register', data={
        'username': 'yenikullanici',
        'email': 'yeni@example.com',
        'password': 'Sifre123',
        'confirm_password': 'Sifre123'
    }, follow_redirects=True)
    
    # Başarılı kayıt sonrası login sayfasına yönlendirme ve flash mesajı beklenir
    assert response.status_code == 200
    assert b'Kayit islemi basarili.' in response.data or b'giri\xc5\x9f yapabilirsiniz' in response.data or b'Kayıt işlemi başarılı' in response.data.decode('utf-8')
    
    with app.app_context():
        user = db.session.scalar(db.select(User).filter_by(username='yenikullanici'))
        assert user is not None
        assert user.email == 'yeni@example.com'

def test_successful_login(client, init_database):
    """Kayıtlı bir kullanıcının doğru şifre ile sisteme giriş yapabildiğini test eder."""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Başarılı giriş sonrası ana sayfadaki elementler veya menü barı beklenir
    assert b'testuser' in response.data or b'Cikis Yap' in response.data or b'Çıkış Yap' in response.data.decode('utf-8')

def test_invalid_login(client, init_database):
    """Yanlış şifre ile sisteme giriş yapılamadığını test eder."""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Hata mesajı beklenir
    decoded_response = response.data.decode('utf-8')
    assert 'Geçersiz kullanıcı adı veya şifre' in decoded_response or 'Gecersiz kullanici' in decoded_response
