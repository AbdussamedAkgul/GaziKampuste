from datetime import date
from app import create_app, db
from app.models import User, Event

events_data = [
    {"title": "Ders Kayıtları", "start": date(2025, 9, 11), "end": date(2025, 9, 15), "type": "school"},
    {"title": "Güz Yarıyılı Başlangıcı", "start": date(2025, 9, 22), "end": None, "type": "school"},
    {"title": "Güz Yarıyılı Dersleri Bitişi", "start": date(2025, 12, 29), "end": None, "type": "school"},
    {"title": "Güz Yarıyılı Dönem Sonu Sınavları (Final)", "start": date(2026, 1, 2), "end": date(2026, 1, 11), "type": "final"},
    {"title": "Güz Yarıyılı Bütünleme Sınavları", "start": date(2026, 1, 19), "end": date(2026, 1, 25), "type": "final"},
    {"title": "Bahar Yarıyılı Başlangıcı", "start": date(2026, 2, 9), "end": None, "type": "school"},
    {"title": "Ortak ve Seçmeli Dersler Ara Sınavları (Vize)", "start": date(2026, 4, 6), "end": date(2026, 4, 10), "type": "midterm"},
    {"title": "Bahar Yarıyılı Dersleri Bitişi", "start": date(2026, 5, 22), "end": None, "type": "school"},
    {"title": "Bahar Yarıyılı Dönem Sonu Sınavları (Final)", "start": date(2026, 6, 1), "end": date(2026, 6, 14), "type": "final"},
    {"title": "Bahar Yarıyılı Bütünleme Sınavları", "start": date(2026, 6, 22), "end": date(2026, 6, 28), "type": "final"}
]

app = create_app()
with app.app_context():
    admin_user = db.session.scalar(db.select(User).where(User.username == 'admin'))
    if not admin_user:
        print("Admin user not found!")
    else:
        for e_data in events_data:
            # Var olup olmadığını kontrol et (tekrar eklemeyi önlemek için)
            existing_event = db.session.scalar(db.select(Event).where(Event.title == e_data["title"], Event.start_date == e_data["start"]))
            if not existing_event:
                new_event = Event(
                    title=e_data["title"],
                    description="2025-2026 Akademik Takvimi",
                    start_date=e_data["start"],
                    end_date=e_data["end"],
                    event_type=e_data["type"],
                    author=admin_user
                )
                db.session.add(new_event)
        
        db.session.commit()
        print("Akademik takvim verileri başarıyla eklendi!")
