import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app import create_app, db
from app.models import CafeteriaMenu, User
import locale
import re

# Ay isimlerini Türkçe eşleştirmek için
tr_months = {
    'ocak': 1, 'şubat': 2, 'mart': 3, 'nisan': 4, 'mayıs': 5, 'haziran': 6,
    'temmuz': 7, 'ağustos': 8, 'eylül': 9, 'ekim': 10, 'kasım': 11, 'aralık': 12
}

def parse_date(date_str):
    # "1 Haziran 2026 Pazartesi" formatını datetime'a çevir
    date_str = date_str.lower().strip()
    parts = date_str.split()
    if len(parts) >= 3:
        try:
            day = int(parts[0])
            month_name = parts[1]
            year = int(parts[2])
            month = tr_months.get(month_name, 1)
            return datetime(year, month, day).date()
        except ValueError:
            pass
    return None

def fetch_and_save_menus():
    url = "https://mediko.gazi.edu.tr/view/page/20412/yemek-listesi"
    try:
        # verify=False for SSL issues that sometimes occur on school networks
        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Hata: Sayfaya erişilemedi - {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Yemek menüsü genellikle sayfanın içindeki tablolarda yer alır.
    tables = soup.find_all('table')
    if not tables:
        print("Tablo bulunamadı!")
        return

    # Sütun bazlı veriyi tutmak için sözlük
    # days_data[col_index] = {'date_obj': None, 'items': [], 'calories': 0}
    days_data = {}

    for table in tables:
        rows = table.find_all('tr')
        if not rows:
            continue
            
        # İlk satır genellikle tarihlerdir
        header_cells = rows[0].find_all(['td', 'th'])
        
        # Eğer bu tablo tarih içermiyorsa atla
        has_date = False
        for cell in header_cells:
            text = cell.get_text(strip=True)
            if any(str(year) in text for year in range(2023, 2030)):
                has_date = True
                break
                
        if not has_date:
            continue
            
        # Sütunları başlat
        current_days_data = {}
        for col_idx, cell in enumerate(header_cells):
            text = cell.get_text(strip=True)
            date_obj = parse_date(text)
            if date_obj:
                current_days_data[col_idx] = {'date_obj': date_obj, 'items': [], 'calories': 0}
                
        # Sonraki satırları oku (yemekler ve kalori)
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            for col_idx, cell in enumerate(cells):
                if col_idx in current_days_data:
                    text = cell.get_text(strip=True)
                    if not text:
                        continue
                    
                    # Kalori kontrolü
                    if 'kcal' in text.lower() or 'kalori' in text.lower() or re.match(r'^\d+\s*(kcal)?$', text.lower()):
                        # Rakamları ayıkla
                        nums = re.findall(r'\d+', text)
                        if nums:
                            current_days_data[col_idx]['calories'] = int(nums[0])
                    else:
                        # Yemek adı
                        current_days_data[col_idx]['items'].append(text)
                        
        # Ana dict'e ekle
        for data in current_days_data.values():
            if data['date_obj']:
                days_data[data['date_obj']] = data
                
    if not days_data:
        print("Geçerli menü verisi çıkarılamadı.")
        return

    print(f"Toplam {len(days_data)} günlük menü bulundu. Veritabanına ekleniyor...")
    
    app = create_app()
    with app.app_context():
        admin_user = db.session.scalar(db.select(User).where(User.username == 'admin'))
        if not admin_user:
            print("Admin kullanıcısı bulunamadı!")
            return
            
        added_count = 0
        updated_count = 0
        
        for date_obj, data in days_data.items():
            if not data['items']:
                continue
                
            items = data['items']
            soup = items[0] if len(items) > 0 else "Belirtilmemiş"
            main_dish = items[1] if len(items) > 1 else "Belirtilmemiş"
            side_dish = ", ".join(items[2:]) if len(items) > 2 else "Belirtilmemiş"
            calories = data['calories']
            
            existing_menu = db.session.scalar(db.select(CafeteriaMenu).where(CafeteriaMenu.date == date_obj))
            
            if existing_menu:
                existing_menu.soup = soup
                existing_menu.main_dish = main_dish
                existing_menu.side_dish = side_dish
                existing_menu.calories = calories
                updated_count += 1
            else:
                new_menu = CafeteriaMenu(
                    date=date_obj,
                    soup=soup,
                    main_dish=main_dish,
                    side_dish=side_dish,
                    calories=calories,
                    author=admin_user
                )
                db.session.add(new_menu)
                added_count += 1
                
        db.session.commit()
        print(f"İşlem tamamlandı! {added_count} yeni gün eklendi, {updated_count} güncellendi.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    fetch_and_save_menus()
