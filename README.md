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
    forms.py         # Profil, Yemekhane ve Duyuru WTForms tanımları [YENİ]
    routes.py        # Ana sayfa, Profil ve CRUD rotaları
  auth/
    __init__.py      # Auth Blueprint tanımlaması
    forms.py         # Giriş, Kayıt ve Şifre Sıfırlama WTForms tanımları
    routes.py        # Giriş/çıkış, kayıt ve şifre sıfırlama rotaları
  models.py          # Veritabanı modelleri (SQLAlchemy 2.0)
  templates/
    base.html        # Jinja2 ana HTML şablonu (Bootstrap 5 & Flash Mesajları)
    index.html       # Dinamik Ana Sayfa şablonu
    profile.html     # Profil düzenleme ve avatar yükleme şablonu [YENİ]
    menus.html       # Yemekhane menüleri listesi [YENİ]
    menu_form.html   # Yemekhane menüsü ekleme/düzenleme formu [YENİ]
    announcements.html # Duyurular listesi [YENİ]
    announcement_form.html # Duyuru ekleme/düzenleme formu [YENİ]
    404.html         # Sayfa Bulunamadı hata şablonu
    500.html         # Beklenmedik sunucu hatası şablonu
    auth/            # Kimlik doğrulama arayüz şablonları
      login.html
      register.html
      reset_password_request.html
      reset_password.html
    search_results.html # Arama sonuçları listeleme sayfası [YENİ]
  static/            # CSS ve görsel dosyaları
    css/
      style.css      # Özelleştirilmiş dark-glassmorphism CSS
    avatars/         # Kullanıcı profil fotoğrafları klasörü
      default.jpg    # Varsayılan kullanıcı avatarı
  translations/      # Flask-Babel Çeviri dosyaları [YENİ]
    en/LC_MESSAGES/
      messages.po
      messages.mo
docs/
  yapay_zeka_gunlugu.md # Yapay Zeka Günlüğü (AI Log)
  proje_raporu.md       # Proje Raporu (Project Report)
migrations/          # Flask-Migrate veritabanı göç dosyaları
tests/               # Birim ve entegrasyon testleri
  test_crud_profile.py # CRUD, Profil ve Sayfalama Otomatik Testleri
config.py            # Uygulama yapılandırma parametreleri
babel.cfg            # Babel çeviri yapılandırması [YENİ]
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

## 🔐 Kimlik Doğrulama, Profil Yönetimi & Güvenlik
* **Şifre Hashleme:** Şifreler veritabanına asla düz metin olarak yazılmaz; `werkzeug.security` ile SHA-256 tabanlı güvenli bir biçimde hashlenir.
* **Form Doğrulama & CSRF:** Tüm formlarda CSRF koruması aktiftir (`form.hidden_tag()`). Formlarda regex doğrulamaları ve veritabanı benzersizlik kontrolleri uygulanmaktadır.
* **Şifre Sıfırlama:** E-posta ile şifre sıfırlama özelliği entegredir. E-postadaki bağlantı 10 dakika geçerli olup, yerel testlerde çıktıları konsola yansıtan mock bir e-posta yapısı kullanılır.
* **Profil Fotoğrafı & Avatar Yükleme:** Kullanıcılar profil fotoğrafı (`avatar`) yükleyebilir. Uzantı doğrulama (.png, .jpg, .jpeg) ve `secure_filename` dosya temizleme kontrolleri barındırır. Yeni fotoğraf yüklendiğinde eski fotoğraf (varsayılan değilse) sunucu diskinden silinir.
* **Yetki Kontrolleri (Ownership):** Yemekhane menüleri ve duyurular sadece onları oluşturan yazarlar tarafından düzenlenebilir veya silinebilir. Yetkisiz isteklerde sistem `403 Forbidden` hatası döndürür.
* **Güvenli Silme İşlemleri:** Silme işlemleri kesinlikle GET isteğiyle yapılamaz; CSRF koruması içeren bir form aracılığıyla POST isteğiyle gerçekleştirilir.

---

## 📄 İçerik Yönetimi (CRUD) & Sayfalama (Pagination)
* **CafeteriaMenu ve Announcement CRUD:** Menüler ve duyurular için Ekle, Listele, Düzenle ve Sil rotaları ve arayüz şablonları tasarlanmıştır.
* **Bootstrap 5 Sayfalama:** Listeleme sayfalarında (menüler ve duyurular) SQLAlchemy `paginate()` metodu kullanılarak sayfa başına 5 kayıt gösterilir. Sayfalama butonları modern glassmorphic tasarıma göre stilize edilmiştir.
* **Dinamik Anasayfa:** Anasayfa (`/`), günün normal ve vejetaryen menülerini ve en son eklenen 3 duyuruyu veritabanından dinamik olarak çeker. Günün menüsü bulunmadığında en son eklenen menüyü geri dönüş (fallback) olarak görüntüler.

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

## 🧪 Otomatik Testlerin Çalıştırılması (Birim Testleri)

Projeyi "production" seviyesine taşımak için kapsamlı bir test altyapısı mevcuttur. Testler, gerçek veritabanını bozmamak adına `in-memory SQLite` (`sqlite:///:memory:`) izole ortamında koşturulur. 

Tüm birim testlerini (CRUD yetkileri, şifreleme mantığı, giriş/kayıt senaryoları) tek bir komutla ve detaylı (verbose) rapor alarak çalıştırmak için terminalde şu komutu girebilirsiniz:

```bash
pytest -v tests/
```

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
