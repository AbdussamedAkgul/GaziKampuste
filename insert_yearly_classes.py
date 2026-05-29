from datetime import date, timedelta
from app import create_app, db
from app.models import User, Event

classes = [
    # 1. Sınıf
    (0, "11:50-14:15", "BLG 103 Web Programlama (1. Sınıf)"),
    (0, "20:30-21:20", "TUR 101 Türk Dili-I (1. Sınıf)"),
    (1, "09:20-11:45", "MOS 111 Zaman Yönetimi (1. Sınıf)"),
    (1, "14:20-16:45", "ISG 101 İş Sağlığı ve Güvenliği (1. Sınıf)"),
    (2, "09:20-11:45", "BLG 109 İşletim Sistemleri (1. Sınıf)"),
    (2, "13:30-15:55", "BLG 107 Bilgisayar Ağları (1. Sınıf)"),
    (3, "09:20-11:45", "BLG 101 Algoritma (1. Sınıf)"),
    (3, "13:30-15:55", "BLG 105 Siber Güvenliğe Giriş (1. Sınıf)"),
    (3, "20:30-21:20", "TAR 101 Atatürk İlke ve İnk. (1. Sınıf)"),
    (4, "09:20-11:45", "ENG 101 İngilizce - I (1. Sınıf)"),
    (4, "13:30-15:55", "MOS 107 Girişimcilik (1. Sınıf)"),
    
    # 2. Sınıf
    (0, "09:20-11:45", "MS 102 Bilgisayar Donanımı (2. Sınıf)"),
    (0, "12:40-15:05", "BLG 203 İleri Ağ Teknolojileri (2. Sınıf)"),
    (1, "09:20-11:45", "BLG 211 Siber Saldırı (2. Sınıf)"),
    (1, "13:30-15:55", "BLG 209 İnternet Programc. (2. Sınıf)"),
    (2, "09:20-11:45", "BLG 205 Veritabanı Uygulamaları (2. Sınıf)"),
    (2, "13:30-15:55", "BLG 207 Kriptoloji (2. Sınıf)"),
    (3, "09:20-11:45", "MS 204 Sayısal Filigranlama (2. Sınıf)"),
    (3, "11:50-13:25", "MS 106 Bilişim Hukuku (2. Sınıf)"),
    (3, "13:30-15:05", "MS 114 E-Ticaret (2. Sınıf)"),
    (4, "13:30-15:55", "ENG 201 İngilizce - III (2. Sınıf)")
]

start_date = date(2026, 1, 1)
end_date = date(2026, 12, 31)

app = create_app()
with app.app_context():
    admin_user = db.session.scalar(db.select(User).where(User.username == 'admin'))
    if not admin_user:
        print("Admin user not found!")
    else:
        # Eski ders programlarını (Güz ve Bahar) temizle ki kopyalar oluşmasın
        db.session.execute(db.delete(Event).where(Event.description.like('%Ders Programı%')))
        db.session.commit()
        
        current_date = start_date
        while current_date <= end_date:
            weekday = current_date.weekday()
            for day_idx, time_str, class_name in classes:
                if day_idx == weekday:
                    title_str = f"[{time_str}] {class_name}"
                    ev = Event(
                        title=title_str,
                        description="Haftalık Ders Programı",
                        start_date=current_date,
                        end_date=None,
                        event_type="school",
                        author=admin_user
                    )
                    db.session.add(ev)
            current_date += timedelta(days=1)
            
        db.session.commit()
        print("Tüm 12 ay için ders programı başarıyla takvime işlendi!")
