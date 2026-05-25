# Gazi Mobil Yönetim Sistemi

Bu proje, **Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı** dersi dönem projesi kapsamında geliştirilen bir web uygulamasıdır. Sistem; öğrencilerin yemekhane menüleri, ders programları ve duyurulara erişebileceği bir platformun yönetim ve bilgi panelini oluşturur.

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
    routes.py        # Giriş/çıkış ve kimlik doğrulama rotaları
  models.py          # Veritabanı modelleri (SQLAlchemy)
  templates/
    base.html        # Jinja2 ana HTML şablonu
  static/            # CSS, JS ve görsel dosyaları
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
   git clone https://github.com/AbdussamedAkgul/gazi-mobil.git
   cd gazi-mobil
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
   SECRET_KEY=gazi-mobil-guvenli-anahtar-1234
   DATABASE_URL=sqlite:///app.db
   FLASK_APP=run.py
   FLASK_DEBUG=1
   ```

5. **Uygulamayı Çalıştırın**:
   ```bash
   python run.py
   ```
   Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışmaya başlayacaktır.
