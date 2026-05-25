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
│   │   └── base.html           # Tüm sayfaların türeyeceği ana şablon
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

## 🗄️ 5. Veritabanı Tasarımı (Planlanan Modeller)

Veritabanında tutulacak tablolar ve aralarındaki ilişkiler şu şekilde planlanmıştır:

1. **User (Kullanıcı Tablosu):**
   * `id` (Primary Key)
   * `username` (Benzersiz Kullanıcı Adı)
   * `email` (Benzersiz E-posta)
   * `password_hash` (Güvenli Şifrelenmiş Parola)
   * `role` (Admin / Editor / Student)

2. **MealMenu (Yemekhane Menüsü Tablosu):**
   * `id` (Primary Key)
   * `date` (Tarih - Benzersiz)
   * `soup` (Çorba)
   * `main_dish` (Ana Yemek)
   * `side_dish` (Yardımcı Yemek)
   * `dessert_or_fruit` (Tatlı veya Meyve)
   * `calories` (Toplam Kalori Değeri)

3. **Announcement (Duyuru Tablosu):**
   * `id` (Primary Key)
   * `title` (Başlık)
   * `content` (Duyuru İçeriği)
   * `created_at` (Oluşturulma Tarihi)
   * `user_id` (Duyuruyu Yayınlayan Editör/Yönetici ID - Foreign Key)

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
4. **Hata Sayfaları (Error Handling):** 404 (Sayfa Bulunamadı) ve 500 (Sunucu Hatası) gibi durumlar için özel şık tasarım hata sayfalarının hazırlanması.

---

## 📈 7. Sonuç ve Değerlendirme

**GaziKampüste Yönetim Sistemi**, modern web geliştirme standartlarına uygun olarak tasarlanmış bir altyapıya sahiptir. Application Factory Pattern ve modüler Blueprint tasarımı sayesinde proje büyüdükçe kod karmaşasının önüne geçilecek, yeni özellikler sisteme çok kolay bir şekilde entegre edilebilecektir.
