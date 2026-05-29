from app import create_app, db
from app.models import User, Event

app = create_app()
with app.app_context():
    # Mevcut tablolara dokunmadan yeni eklenen tabloları oluşturur
    db.create_all()
    
    admin_user = db.session.scalar(db.select(User).where(User.username == 'admin'))
    if not admin_user:
        admin_user = User(username='admin', email='admin@gazi.edu.tr', role='admin')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        admin_user.role = 'admin'
        admin_user.set_password('admin123')
        db.session.commit()
        print("Admin user updated successfully!")
