# GaziKampüste

Bu proje, **Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı** dersi dönem projesi kapsamında geliştirilen bir web uygulamasıdır. Sistem; öğrencilerin yemekhane menüleri, ders programları ve duyurulara erişebileceği bir platformun yönetim ve bilgi panelini (GaziKampüste Yönetim Sistemi) oluşturur.

## 🚀 Proje Mimarisi: Application Factory Pattern & Blueprints

Proje, Flask topluluğu tarafından önerilen modern ve sürdürülebilir **Application Factory Pattern** (Uygulama Fabrikası Şablonu) ve **Blueprint** (Modüler Yapı) yaklaşımı kullanılarak sıfırdan tasarlanmıştır. Bu yapı projenin ölçeklenebilirliğini artırır ve modüller (örneğin auth, main) arasında döngüsel bağımlılıkların (circular import) oluşmasını engeller.

### Dizin Yapısı

```text
app/
  __init__.py        # Flask Uygulama Fabrikası (create_app) ve eklentilerin başlangıcı
  main/
    __init__.py      # Main Blueprint tanımlaması
    routes.py        # Ana sayfa ve genel rota tanımlamaları
  auth/
    __init__.py      # Auth Blueprint tanımlaması
    forms.py         # Giriş, Kayıt ve Şifre Sıfırlama WTForms tanımları
    routes.py        # Giriş/çıkış, kayıt ve şifre sıfırlama rotaları
  models.py          # Veritabanı modelleri (SQLAlchemy 2.0)
  templates/
    base.html        # Jinja2 ana HTML şablonu (Bootstrap 5 & Flash Mesajları)
    404.html         # Sayfa Bulunamadı hata şablonu
    500.html         # Beklenmedik sunucu hatası şablonu
    auth/            # Kimlik doğrulama arayüz şablonları
      login.html
      register.html
      reset_password_request.html
      reset_password.html
  static/            # CSS, JS ve görsel dosyaları
docs/
  yapay_zeka_gunlugu.md # Yapay Zeka Günlüğü (AI Log)
  proje_raporu.md       # Proje Raporu (Project Report)
migrations/          # Flask-Migrate veritabanı göç dosyaları
tests/               # Birim ve entegrasyon testleri
config.py            # Uygulama yapılandırma parametreleri
requirements.txt     # Gerekli Python kütüphaneleri listesi
.env.example         # Örnek çevre değişkenleri şablonu
.env                 # Yerel çevre değişkenleri (Veritabanı URI, Gizli Anahtar vb.)
.gitignore           # Git'e eklenmeyecek dosyalar listesi
run.py               # Uygulamayı başlatan ana giriş noktası
```

---

## 🗄️ Veritabanı Modelleri

Uygulamada kullanılan veritabanı şeması ve modelleri **SQLAlchemy 2.0** standartlarında (`Mapped` ve `mapped_column`) [app/models.py](file:///c:/Users/AKGUL/Desktop/Abd%C3%BCssamed/Gazi%20Ders/GaziMobilFinalEdizHoca/app/models.py) içinde tanımlanmıştır:

1. **User (Kullanıcı)**: Kullanıcı bilgilerini (öğrenci, editör, yönetici rolleriyle) saklar. Şifre güvenliği `werkzeug.security` (`set_password`/`check_password`) ile gerçekleştirilir. `Flask-Login` uyumludur. E-posta şifre sıfırlama akışı için `itsdangerous` ile süreli token entegrasyonuna sahiptir.
2. **CafeteriaMenu (Yemekhane Menüsü)**: Günlük yemek listelerini tutar. Aynı gün için hem normal hem de vejetaryen menü girişini destekler.
3. **Announcement (Duyuru)**: Kampüs ve yüksekokul duyurularını saklar.

*Modeller arasındaki Bire-Çok (One-to-Many) ilişkiler kurulmuş ve ilişkili silme işlemleri (`cascade="all, delete-orphan"`) yapılandırılmıştır.*

---

## 🔐 Kimlik Doğrulama & Güvenlik
* **Şifre Hashleme:** Şifreler veritabanına asla düz metin olarak yazılmaz; `werkzeug.security` ile SHA-256 tabanlı güvenli bir biçimde hashlenir.
* **Form Doğrulama & CSRF:** Tüm formlarda CSRF koruması aktiftir. Formlarda kullanıcı adı regex doğrulaması (sadece harf, rakam, `.`, `_`) ve e-posta biçim kontrolleri yapılmaktadır.
* **Şifre Sıfırlama:** E-posta ile şifre sıfırlama özelliği entegredir. E-postadaki bağlantı 10 dakika geçerli olup, yerel testlerde çıktıları konsola yansıtan mock bir e-posta yapısı kullanılır.

---

## 🛠️ Kullanılan Teknolojiler

Projede sadece aşağıda belirtilen temel kütüphaneler kullanılmıştır:
* **Flask 3.x**: Web uygulama çatısı
* **Flask-SQLAlchemy**: Veritabanı işlemleri ve ORM yönetimi
* **Flask-Migrate**: Veritabanı şeması göç işlemleri
* **Flask-Login**: Kullanıcı giriş/çıkış ve oturum yönetimi
* **Flask-WTF**: Güvenli form işlemleri ve CSRF koruması
* **python-dotenv**: `.env` dosyasındaki çevre değişkenlerinin yönetimi
* **SQLite**: Hafif ve taşınabilir yerel veritabanı


---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Projeyi Klonlayın**:
   ```bash
   git clone https://github.com/AbdussamedAkgul/GaziKampuste.git
   cd GaziKampuste
   ```

2. **Sanal Ortam Oluşturun ve Aktifleştirin**:
   ```bash
   # Windows için:
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux için:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Bağımlılıkları Yükleyin**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Çevre Değişkenlerini Ayarlayın**:
   `.env.example` dosyasının adını `.env` olarak değiştirin veya kopyalayın, ardından içeriğini projenize göre düzenleyin:
   ```text
   SECRET_KEY=gazi-kampuste-guvenli-anahtar-1234
   DATABASE_URL=sqlite:///app.db
   FLASK_APP=run.py
   FLASK_DEBUG=1
   ```

5. **Uygulamayı Çalıştırın**:
   ```bash
   python run.py
   ```
   Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışmaya başlayacaktır.
