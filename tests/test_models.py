from app.models import User

def test_password_hashing():
    """Kullanıcı şifreleme ve doğrulama fonksiyonlarının düzgün çalıştığını kontrol eder."""
    u = User(username='ahmet', email='ahmet@example.com')
    u.set_password('gizli_sifre')
    
    # Şifre hash'inin orijinal şifre ile aynı olmadığını doğrula
    assert u.password_hash != 'gizli_sifre'
    
    # Doğru şifre ile kontrol edildiğinde True dönmeli
    assert u.check_password('gizli_sifre') is True
    
    # Yanlış şifre ile kontrol edildiğinde False dönmeli
    assert u.check_password('yanlis_sifre') is False

def test_avatar_default_value():
    """Yeni oluşturulan bir kullanıcının varsayılan avatar dosyasının 'default.jpg' olduğunu kontrol eder."""
    u = User(username='mehmet', email='mehmet@example.com')
    assert u.avatar_file == 'default.jpg'
