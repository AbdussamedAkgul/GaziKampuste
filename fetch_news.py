import requests
from bs4 import BeautifulSoup
from datetime import date
from app import create_app, db
from app.models import Announcement, User

def fetch_and_save_news():
    url = "https://kazanmyo.gazi.edu.tr/"
    try:
        response = requests.get(url, verify=False, timeout=10) # Bazen SSL sorunları olabiliyor, verify=False ekledik
        response.raise_for_status()
    except Exception as e:
        print(f"Hata: Sayfaya erişilemedi - {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Haberleri bul (Genellikle "announcement-list" veya ilgili class'ta olur)
    # Gazi web siteleri genellikle belirli css sınıflarına sahiptir: e.g. .post-content, .news-title vb.
    # Siteyi genel analiz edip linkleri toplayalım. A etiketleri içinde title veya aria-label olanları haber sayabiliriz.
    
    items = soup.find_all('a', href=True)
    news_titles = set()
    news_data = []
    
    for item in items:
        href = item['href']
        # 'view/announcement' içeren linkler haber veya duyurudur
        if '/view/announcement/' in href:
            title = item.get('title') or item.get_text(strip=True)
            if title and len(title) > 5 and title not in news_titles:
                news_titles.add(title)
                full_url = href if href.startswith('http') else f"https://kazanmyo.gazi.edu.tr{href}"
                content = f"Daha fazla bilgi için <a href='{full_url}' target='_blank'>orijinal sayfaya gidin</a>."
                news_data.append({'title': title, 'content': content})
    
    if not news_data:
        print("Sayfadan haber veya duyuru çıkarılamadı!")
        return
        
    print(f"Toplam {len(news_data)} haber bulundu. Veritabanına ekleniyor...")
    
    app = create_app()
    with app.app_context():
        admin_user = db.session.scalar(db.select(User).where(User.username == 'admin'))
        if not admin_user:
            print("Admin kullanıcısı bulunamadı!")
            return
            
        # Zaten eklenmiş olanları atlamak için
        existing_titles = set(db.session.scalars(db.select(Announcement.title)).all())
        
        added_count = 0
        for data in news_data:
            if data['title'] not in existing_titles:
                announcement = Announcement(
                    title=data['title'],
                    content=data['content'],
                    date=date.today(),
                    author=admin_user
                )
                db.session.add(announcement)
                added_count += 1
                
        db.session.commit()
        print(f"İşlem tamamlandı! {added_count} yeni duyuru eklendi.")

if __name__ == "__main__":
    # InsecureRequestWarning gizlemek için
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    fetch_and_save_news()
