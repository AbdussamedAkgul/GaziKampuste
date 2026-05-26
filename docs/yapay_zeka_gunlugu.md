# Yapay Zeka Günlüğü (AI Log)

Bu günlük, **GaziKampüste Yönetim Sistemi** geliştirilirken kullanılan yapay zeka araçları (Gemini), girilen istemler (prompts) ve projeye olan katkılarını belgelemek amacıyla tutulmaktadır.

---

### 📅 Günlük Kaydı: 25 Mayıs 2026

#### 🎯 Yapılan İş / Hedef:
Flask 3.x tabanlı projenin temel mimarisini "Application Factory Pattern" ve "Blueprint" yapılarına uygun olarak sıfırdan kurmak.

#### 💬 Yapay Zekaya Gönderilen İstem (Prompt):
> "Bağlam: Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı dersi dönem projem için Flask 3.x tabanlı bir web uygulaması geliştireceğim. Projemin adı "Gazi Kampüste Yönetim Sistemi". Bu sistem, öğrencilerin yemekhane menülerine, ders programlarına ve duyurulara ulaşabileceği bir platformun yönetim ve bilgi paneli olacak. 
> 
> Hedef: Projenin temel mimarisini "Application Factory Pattern" yapısına uygun ve Blueprint'ler kullanacak şekilde sıfırdan kur. Klasör yapısının aynen şu şekilde olmasını istiyorum:
> app/
>   __init__.py
>   main/
>     __init__.py
>     routes.py
>   auth/
>     __init__.py
>     routes.py
>   models.py
>   templates/
>     base.html
>   static/
> migrations/
> tests/
> config.py
> requirements.txt
> .env.example
> .gitignore
> run.py"

#### 🤖 Yapay Zekanın Katkısı / Çözümü:
1. **Dizin ve Dosya Yapılandırması**: İstediğim dizin yapısı sırasıyla oluşturuldu.
2. **Kütüphanelerin Listelenmesi**: `requirements.txt` dosyasına sadece talep ettiğim altı kütüphane eklendi: `flask`, `flask-sqlalchemy`, `flask-migrate`, `flask-login`, `flask-wtf`, `python-dotenv`.
3. **Application Factory Kurulumu**: `app/__init__.py` içinde `create_app` fonksiyonu ile Flask nesnesi ve eklentileri (SQLAlchemy, Migrate, LoginManager) initialize edildi.
4. **Blueprint Entegrasyonu**: `auth` ve `main` için ayrı ayrı Blueprint tanımlamaları yapıldı ve fabrikaya kaydedildi.
5. **Güvenlik & Git**: Yerel çevre değişkenleri için `.env` ve `.env.example` oluşturulup `.env` dosyası doğrudan `.gitignore` dosyasında dışlandı.

#### 💡 Kazanım:
* Flask projelerinde büyük ölçekli ve modüler kod tasarımı için kullanılan **Application Factory Pattern** yapısının pratik uygulamasını öğrendim.
* Blueprint yapısı ile modül ilişkilerini ayırıp, rotaları mantıksal gruplara bölerek çakışmaları ve döngüsel bağımlılık (circular import) hatalarını engellemiş oldum.

---

### 📅 Günlük Kaydı: 26 Mayıs 2026

#### 🎯 Yapılan İş / Hedef:
Veritabanı modellerinin (`User`, `CafeteriaMenu`, `Announcement`) SQLAlchemy 2.0 stili (`Mapped`, `mapped_column`) kullanılarak tanımlanması ve ilişkilerinin kurulması.

#### 💬 Yapay Zekaya Gönderilen İstem (Prompt):
> "Bağlam: GaziKampuste projemizin ikinci oturumuna geçiyoruz. İlk oturumda application factory iskeletini kurduk, app/__init__.py içinde db = SQLAlchemy() tanımlandı. Veritabanı olarak şimdilik SQLite kullanacağız, config.py içinde SQLALCHEMY_DATABASE_URI ayarlı. Henüz hiç model yok.
> 
> Hedef: app/models.py dosyasını oluştur (veya varsa içine yaz) ve şu 3 modeli tanımla:
> 1. User: id, username, email, password_hash, role (default 'student'), avatar_file (ileride eklenecek profil resmi için, default 'default.jpg'), created_at.
> 2. CafeteriaMenu: id, date, soup, main_dish, side_dish, calories, user_id (Bunu ekleyen kullanıcının FK'sı).
> 3. Announcement: id, title, content, date, user_id (Bunu oluşturan kullanıcının FK'sı).
> 
> İlişkiler:
> - User -> CafeteriaMenu : One-to-Many
> - User -> Announcement : One-to-Many
> 
> Kısıtlar:
> - KESİNLİKLE SQLAlchemy 2.x stilini kullan (Mapped, mapped_column kullan; kesinlikle eski nesil db.Column kullanma).
> - User modeli içerisine werkzeug.security kullanarak check_password ve set_password metotlarını ekle.
> - Tüm modellere okunaklı __repr__ metotları ekle.
> - Henüz terminalde hiçbir migration (flask db) komutu ÇALIŞTIRMA; sadece modelleri yaz.
> - Geri Bildirim: Bir günde hem normal hem de vejetaryen menü girilebilmesi için date benzersiz olmamalı. Zaman tipi olarak sadece tarih tutan Date kullanılmalı."

#### 🤖 Yapay Zekanın Katkısı / Çözümü:
1. **SQLAlchemy 2.0 Declarative Mapping**: Modeller `db.Model` sınıfından türetilerek, sütun tanımlamaları modern `Mapped[...]` ve `mapped_column(...)` sözdizimiyle gerçekleştirildi.
2. **Kullanıcı Şifre Güvenliği**: `User` modeline `werkzeug.security` paketinden `generate_password_hash` ve `check_password_hash` işlevleri entegre edilerek `set_password` ve `check_password` metotları yazıldı.
3. **İlişkiler ve Cascade Ayarları**: `User` ile `CafeteriaMenu` ve `Announcement` arasındaki bire-çok (One-to-Many) ilişkiler `relationship(back_populates=...)` ve `cascade="all, delete-orphan"` özellikleri kullanılarak çift yönlü tanımlandı.
4. **Tarih Tipi Uyumlaştırma**: Kullanıcının isteği üzerine hem menüler hem de duyurular için saat bilgisi barındırmayan `Date` veri tipi kullanıldı ve varsayılan değer olarak `date.today` tanımlandı. Yemek menüsünde çakışma olmaması için `unique` kısıtı kaldırılıp, menüleri ayırt etmek amacıyla `menu_type` (normal/vegetarian) alanı eklendi.
5. **Flask-Login Entegrasyonu**: Uygulamanın login mimarisiyle doğrudan uyumlu çalışabilmesi için `User` modeline `UserMixin` dahil edildi.

#### 💡 Kazanım:
* SQLAlchemy 2.x ile gelen tip güvenli `Mapped` ve `mapped_column` kullanımının avantajlarını ve yeni deklaratif yapısını kavradım.
* Veritabanı tasarımında iş kurallarına göre (örn: aynı gün hem normal hem vejetaryen menü olabilmesi) benzersizlik (unique) kısıtlarının ve ek alanların (`menu_type`) nasıl şekillendirileceğini öğrendim.
* İlişkili tablolarda cascade (silme/güncelleme yayılımı) mekanizmasının SQLAlchemy ORM düzeyinde nasıl yapılandırıldığını uyguladım.
