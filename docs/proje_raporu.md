# 📝 GaziKampüste Yönetim Sistemi - Proje Raporu

Bu rapor, **Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı** dersi dönem projesi kapsamında geliştirilen **GaziKampüste Yönetim Sistemi**'nin teknik altyapısını, mimari kararlarını, kullanılan teknolojileri ve gelecek planlamalarını detaylandırmaktadır.

---

## 📌 1. Proje Hakkında ve Amaç

**GaziKampüste Yönetim Sistemi**, Gazi Üniversitesi öğrencilerinin ve akademik/idari personelinin kampüs yaşamını kolaylaştırmayı amaçlayan dinamik bir web uygulamasıdır. 

Sistemin temel hedefleri şunlardır:
* **Yemekhane Menüsü Takibi:** Günlük ve haftalık yemek menülerinin yönetim paneli üzerinden girilmesi ve öğrencilere sunulması.
* **Duyuru Yönetimi:** Bölüm, yüksekokul ve üniversite genelindeki duyuruların tek bir merkezden duyurulması.
* **Ders Programı Bilgilendirmesi:** Öğrencilerin ve öğretim görevlilerinin ders programlarına kolayca erişebilmesi.
* **Kullanıcı Yetkilendirme:** Yönetici (Admin), Editör ve Öğrenci rolleri ile sistem güvenliği ve veri yönetiminin kontrol altında tutulması.

---

## 🏗️ 2. Mimari Tasarım ve Tasarım Kalıpları

Uygulamanın sürdürülebilir, test edilebilir ve genişletilebilir olması amacıyla Flask topluluğu tarafından önerilen en iyi pratikler benimsenmiştir:

### ⚙️ Application Factory Pattern (Uygulama Fabrikası Şablonu)
Flask uygulaması, küresel düzeyde tek bir `app` nesnesi oluşturmak yerine `app/__init__.py` içerisinde tanımlanan `create_app()` fonksiyonu ile dinamik olarak ayağa kaldırılır.
* **Avantajları:**
  * Farklı yapılandırmalar (Test, Geliştirme, Üretim) için kolayca farklı uygulama örnekleri oluşturulabilir.
  * Döngüsel bağımlılık (circular import) hatalarının önüne geçilir.
  * Kodun test edilebilirliği artar.

### 🧩 Blueprints (Modüler Rota Yönetimi)
Uygulama işlevsel olarak mantıksal modüllere bölünmüştür. Şu an için tanımlanmış modüller:
1. **`main` (Ana Modül):** Ana sayfa, genel bilgiler, ders programı ve yemekhane menüsü gibi herkese açık rotaları içerir.
2. **`auth` (Kimlik Doğrulama Modülü):** Giriş yapma, çıkış yapma, şifre değiştirme ve kayıt olma gibi kullanıcı işlemlerini yönetir.

---

## 📂 3. Klasör Yapısı ve Dosya Açıklamaları

Proje dosyaları modülerlik ilkesine uygun olarak aşağıdaki gibi yapılandırılmıştır:

```text
GaziKampuste/
│
├── app/                        # Ana Uygulama Klasörü
│   ├── __init__.py             # Flask Uygulama Fabrikası (create_app) ve eklentilerin ilklendirilmesi
│   ├── models.py               # Veritabanı Modelleri (Kullanıcı, Yemekhane, Duyuru vb.)
│   │
│   ├── main/                   # Genel İşlevler ve Rotalar Modülü
│   │   ├── __init__.py         # Main Blueprint tanımı
│   │   └── routes.py           # Ana sayfa ve genel görünüm rotaları
│   │
│   ├── auth/                   # Kimlik Doğrulama Modülü
│   │   ├── __init__.py         # Auth Blueprint tanımı
│   │   └── routes.py           # Giriş, çıkış ve kayıt rotaları
│   │
│   ├── templates/              # Jinja2 HTML Şablonları
│   │   ├── base.html           # Tüm sayfaların türeyeceği ana şablon
│   │   ├── 404.html            # Sayfa Bulunamadı hata şablonu
│   │   └── 500.html            # Beklenmedik sunucu hatası şablonu
│   │
│   └── static/                 # Statik Dosyalar (CSS, JS, Görseller)
│
├── docs/                       # Belgelendirme
│   ├── yapay_zeka_gunlugu.md   # Yapay zeka kullanım süreçleri günlüğü
│   └── proje_raporu.md         # Mevcut proje raporu (Bu dosya)
│
├── migrations/                 # Veritabanı Şeması Geçiş Dosyaları (Flask-Migrate)
├── tests/                      # Birim ve Entegrasyon Testleri
├── config.py                   # Uygulama Yapılandırma Sınıfı (Config)
├── requirements.txt            # Python Bağımlılıkları Listesi
├── .env                        # Hassas Bilgiler ve Çevre Değişkenleri (Lokal)
├── .env.example                # Çevre Değişkenleri Şablonu
├── .gitignore                  # Git Versiyon Kontrolüne Dahil Edilmeyecekler
└── run.py                      # Uygulamayı Başlatan Giriş Noktası
```

---

## 🛠️ 4. Kullanılan Teknolojiler ve Kütüphaneler

Projede gereksiz bağımlılıklardan kaçınılarak sadece projenin temel gereksinimlerini karşılayan, modern ve hafif kütüphaneler tercih edilmiştir:

| Kütüphane / Teknoloji | Sürüm | Açıklama |
| :--- | :--- | :--- |
| **Flask** | `3.x` | Ana web çatısı (Web framework). |
| **Flask-SQLAlchemy** | En güncel | Veritabanı erişimi ve nesne ilişkisel eşleme (ORM) yönetimi. |
| **Flask-Migrate** | En güncel | Veritabanı şeması değişikliklerini izleme ve versiyonlama (Alembic tabanlı). |
| **Flask-Login** | En güncel | Güvenli kullanıcı oturum yönetimi, giriş/çıkış kontrolü. |
| **Flask-WTF** | En güncel | Form doğrulama, görsel alan yönetimi ve CSRF güvenliği. |
| **python-dotenv** | En güncel | Hassas bilgilerin `.env` dosyasından okunması. |
| **SQLite** | Dahili | Yerel geliştirme için hafif ve dosya tabanlı ilişkisel veritabanı. |

---

## 🗄️ 5. Veritabanı Tasarımı (Gerçekleştirilen ve Planlanan Modeller)

Veritabanı tasarımı, modern **SQLAlchemy 2.0** (Mapped, mapped_column) standartlarına uygun şekilde yapılmıştır. Gerçekleştirilen modeller ve planlanan diğer tablolar şu şekildedir:

### 🟢 Gerçekleştirilen Modeller

1. **User (Kullanıcı Tablosu - `users`):**
   * `id`: `Mapped[int]` (Primary Key)
   * `username`: `Mapped[str]` (Benzersiz Kullanıcı Adı, Index, String(64))
   * `email`: `Mapped[str]` (Benzersiz E-posta, Index, String(120))
   * `password_hash`: `Mapped[str]` (Parola Hash Değeri, String(256))
   * `role`: `Mapped[str]` (Rol - student/editor/admin, varsayılan: 'student', String(20))
   * `avatar_file`: `Mapped[str]` (Profil Resmi Dosya Adı, varsayılan: 'default.jpg', String(64))
   * `created_at`: `Mapped[date]` (Oluşturulma Tarihi, varsayılan: `date.today`, Date)
   * **İlişkiler:** `menus` (CafeteriaMenu ile Bire-Çok), `announcements` (Announcement ile Bire-Çok)

2. **CafeteriaMenu (Yemekhane Menüsü Tablosu - `cafeteria_menus`):**
   * `id`: `Mapped[int]` (Primary Key)
   * `date`: `Mapped[date]` (Menü Tarihi, Index, Date)
   * `menu_type`: `Mapped[str]` (Menü Türü - normal/vegetarian, varsayılan: 'normal', String(20))
   * `soup`: `Mapped[str]` (Çorba, String(100))
   * `main_dish`: `Mapped[str]` (Ana Yemek, String(100))
   * `side_dish`: `Mapped[str]` (Yardımcı Yemek, String(100))
   * `calories`: `Mapped[Optional[int]]` (Kalori Değeri, Nullable)
   * `user_id`: `Mapped[int]` (Ekleyen Kullanıcı ID - Foreign Key -> `users.id`)
   * **İlişkiler:** `author` (User ile Çok-Bir)

3. **Announcement (Duyuru Tablosu - `announcements`):**
   * `id`: `Mapped[int]` (Primary Key)
   * `title`: `Mapped[str]` (Başlık, String(100))
   * `content`: `Mapped[str]` (Duyuru İçeriği, Text)
   * `date`: `Mapped[date]` (Yayınlanma Tarihi, varsayılan: `date.today`, Date)
   * `user_id`: `Mapped[int]` (Yayınlayan Kullanıcı ID - Foreign Key -> `users.id`)
   * **İlişkiler:** `author` (User ile Çok-Bir)

### 🟡 Planlanan Modeller

4. **ClassSchedule (Ders Programı Tablosu):**
   * `id` (Primary Key)
   * `department` (Bölüm Adı)
   * `class_name` (Sınıf / Derslik)
   * `day_of_week` (Gün)
   * `start_time` - `end_time` (Saat Aralığı)
   * `subject` (Ders Adı)
   * `instructor` (Öğretim Görevlisi)

---

## 🔐 6. Kimlik Doğrulama, Profil Yönetimi ve Güvenlik Akışları

Projenin 3. ve 4. oturumlarında, güvenli ve tam fonksiyonel bir kullanıcı yönetim sistemi ve profil altyapısı kurulmuştur. Bu sistem kapsamında aşağıdaki mekanizmalar uygulanmıştır:

### 🔑 Şifre Güvenliği ve Hashleme
Kullanıcı şifreleri veritabanına asla düz metin (plain text) olarak kaydedilmez. `User` modeli üzerinde `werkzeug.security` kütüphanesinin `generate_password_hash` ve `check_password_hash` metotları kullanılarak şifreler SHA-256 algoritmasıyla güvenli bir şekilde hashlenir ve doğrulanır.

### 🛡️ CSRF, Form Güvenliği ve Avatar Yükleme
Flask-WTF ve WTForms kütüphaneleri kullanılarak geliştirilen tüm form yapılarında (`RegisterForm`, `LoginForm`, `ResetPasswordRequestForm`, `ResetPasswordForm`, `ProfileForm`, `CafeteriaMenuForm`, `AnnouncementForm`) CSRF (Cross-Site Request Forgery) koruması (`form.hidden_tag()`) zorunlu kılınmıştır.
* **Profil Güncelleme ve Avatar Yükleme:** Kullanıcılar profil bilgilerini `/profile` sayfasından güncelleyebilirler. `secure_filename` ve `FileAllowed` yardımıyla sadece `.png`, `.jpg`, `.jpeg` uzantılarına izin verilir. Yüklenen fotoğraflar `app/static/avatars/` klasörüne zaman damgalı tekil isimlerle kaydedilir. Önbellekleme sorunları önlenir ve eski avatar dosyası (varsayılan değilse) sunucu diskinden temizlenir.

### 📧 E-Posta ile Şifre Sıfırlama (Bonus Özellik)
Kullanıcıların şifrelerini unutmaları durumunda e-posta adreslerine güvenli bir sıfırlama bağlantısı gönderilir.
* **Token Güvenliği:** `itsdangerous.URLSafeTimedSerializer` kullanılarak her sıfırlama talebi için kullanıcının ID'sini içeren ve 10 dakika geçerliliği olan imzalı, güvenli bir token üretilir.
* **Mock Servisi:** Yerel testlerin kolay yapılabilmesi için gerçek bir SMTP sunucusu yerine, gönderilen e-postanın içeriğini ve sıfırlama bağlantısını doğrudan terminal konsoluna yazdıran bir mock e-posta gönderim yapısı kurulmuştur.

---

## 🍴 7. İçerik Yönetimi (CRUD), Yetkilendirme ve Sayfalama (4. Oturum)

Uygulamanın ana içerik yönetim altyapısını oluşturan yemekhane menüleri ve duyurular için tam teşekküllü yönetim işlevleri entegre edilmiştir:

### 📝 Tam CRUD Desteği
`CafeteriaMenu` ve `Announcement` modelleri için ekleme, listeleme, düzenleme ve silme özellikleri rotalarla birlikte geliştirilmiştir. Form kontrolleri ve validasyonlar Flask-WTF ile sağlanmaktadır.

### 🛑 Yetki ve Sahiplik Kontrolü
Bir yemekhane menüsünü veya duyuruyu **sadece onu oluşturan yazar (sahibi)** düzenleyebilir veya silebilir. Başka bir kullanıcının bu işlemleri yapma veya doğrudan URL üzerinden erişim sağlama girişimlerinde `403 Forbidden` hata kodu döndürülür.

### 🧼 Güvenli Kayıt Silme
Silme işlemleri kesinlikle GET isteğiyle tetiklenemez. CSRF koruması içeren bir gizli form üzerinden, kullanıcıdan onay alınarak **POST** istekleriyle çalışır.

### 📄 Bootstrap 5 ile Sayfalama
SQLAlchemy ORM'in `paginate()` metodu kullanılarak menüler (`/menus`) ve duyurular (`/announcements`) sayfalarında **sayfa başına 5 kayıt** gösterilmektedir. Sayfalama butonları koyu glassmorphism tasarımına özel Bootstrap 5 yapısında tasarlanmıştır.

### 🧪 Otomatik Birim Testleri (Automated Tests)
Geliştirilen tüm CRUD yetkilendirme akışlarını, profile resim yükleme kurallarını ve sayfalama sınırlarını doğrulamak üzere `tests/test_crud_profile.py` test sınıfı yazılmıştır. Python'ın yerleşik `unittest` modülüyle çalıştırılan testler başarıyla geçmiştir (`OK`).

---

## 🔮 8. Gelecek Geliştirme Adımları

Geliştirme sürecinin bir sonraki aşamalarında gerçekleştirilmesi planlanan işler şunlardır:
1. **Ders Programı Modülü (ClassSchedule):** Öğrencilerin ve akademik personelin haftalık ders programlarını görebileceği veritabanı tablolarının ve arayüzünün oluşturulması.
2. **Kullanıcı Rol Yönetimi:** Adminlerin kullanıcı rollerini (`student`, `editor`, `admin`) yönetebileceği bir admin panel ara yüzünün tasarlanması.

---

## 📈 9. Sonuç ve Değerlendirme

**GaziKampüste Yönetim Sistemi**, modern web standartlarına uygun, güvenli ve modüler bir mimariyle geliştirilmektedir. Son oturumla birlikte entegre edilen profil yönetimi, güvenli CRUD akışları, sahiplik yetki kontrolleri ve sayfalama sistemi sayesinde uygulamanın omurgası tamamlanmıştır. Yazılan otomatik birim testleri sistemin yüksek kalitede ve hatasız çalıştığını güvence altına almaktadır. Modüler Blueprint tasarımı projenin gelecekte rahatça büyümesine imkan tanımaktadır.

