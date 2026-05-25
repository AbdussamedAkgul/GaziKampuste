# Yapay Zeka Günlüğü (AI Log)

Bu günlük, **Gazi Mobil Yönetim Sistemi** geliştirilirken kullanılan yapay zeka araçları (Gemini), girilen istemler (prompts) ve projeye olan katkılarını belgelemek amacıyla tutulmaktadır.

---

### 📅 Günlük Kaydı: 25 Mayıs 2026

#### 🎯 Yapılan İş / Hedef:
Flask 3.x tabanlı projenin temel mimarisini "Application Factory Pattern" ve "Blueprint" yapılarına uygun olarak sıfırdan kurmak.

#### 💬 Yapay Zekaya Gönderilen İstem (Prompt):
> "Bağlam: Gazi Üniversitesi TUSAŞ Kazan Meslek Yüksekokulu İnternet Programcılığı dersi dönem projem için Flask 3.x tabanlı bir web uygulaması geliştireceğim. Projemin adı "Gazi Mobil Yönetim Sistemi". Bu sistem, öğrencilerin yemekhane menülerine, ders programlarına ve duyurulara ulaşabileceği bir platformun yönetim ve bilgi paneli olacak. 
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
* Blueprint yapısı ile modülleri ayırıp, rotaları mantıksal gruplara bölerek çakışmaları ve döngüsel bağımlılık (circular import) hatalarını engellemiş oldum.
