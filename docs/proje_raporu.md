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

## 🔮 6. Gelecek Geliştirme Adımları

Geliştirme sürecinin bir sonraki aşamalarında gerçekleştirilmesi planlanan işler sırasıyla şunlardır:
1. **Şablon Tasarımları (Frontend):** Modern, mobil uyumlu (responsive) ve Gazi Üniversitesi renk temasına uygun bir kullanıcı arayüzü (UI) geliştirilmesi.
2. **Kullanıcı Giriş Sistemi Aktivasyonu:** `Flask-Login` kullanılarak şifre hashleme (`werkzeug.security`) mekanizmasıyla giriş/çıkış işlemlerinin tamamlanması.
3. **Yönetim Paneli (Admin Panel):** Yönetici ve editörlerin veritabanına yeni yemek listesi, duyuru ve ders programı ekleyebileceği formların ve tabloların oluşturulması.

*(Not: Hata Sayfaları (Error Handling) bu oturumda tamamlanmış, 404 ve 500 hata durumları şablonlarıyla birlikte sisteme entegre edilmiştir.)*

---

## 📈 7. Sonuç ve Değerlendirme

**GaziKampüste Yönetim Sistemi**, modern web geliştirme standartlarına uygun olarak tasarlanmış bir altyapıya sahiptir. Application Factory Pattern ve modüler Blueprint tasarımı sayesinde proje büyüdükçe kod karmaşasının önüne geçilecek, yeni özellikler sisteme çok kolay bir şekilde entegre edilebilecektir.
