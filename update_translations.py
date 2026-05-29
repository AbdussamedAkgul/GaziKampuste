import os
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import write_mo

translations = {
    "Gazi Üniversitesi Kampüs": "Gazi University Campus",
    "Yönetim Sistemi": "Management System",
    "Öğrenciler ve personel için yemekhane menüsü takibi, ders programı bilgilendirmesi ve anlık duyurular tek bir güvenli panelde.": "Cafeteria menu tracking, course schedule updates, and instant announcements for students and staff in a single secure panel.",
    "Profilimi Yönet": "Manage My Profile",
    "Yemekhane Menüsü": "Cafeteria Menu",
    "Günün Yemekhane Menüsü": "Today's Cafeteria Menu",
    "Çorba": "Soup",
    "Ana Yemek": "Main Dish",
    "Yardımcı Yemek": "Side Dish",
    "Toplam Enerji": "Total Energy",
    "Bugün için menü girişi yapılmamıştır.": "No menu has been entered for today.",
    "Son Duyurular": "Latest Announcements",
    "Henüz yayınlanmış bir duyuru bulunmamaktadır.": "No announcements have been published yet.",
    "Yemekhane Menüleri": "Cafeteria Menus",
    "Yeni Menü Ekle": "Add New Menu",
    "Düzenle": "Edit",
    "Sil": "Delete",
    "Bu yemekhane menüsünü silmek istediğinize emin misiniz?": "Are you sure you want to delete this cafeteria menu?",
    "Henüz eklenmiş bir yemekhane menüsü bulunmamaktadır.": "No cafeteria menu has been added yet.",
    "Haberler ve Duyurular": "News and Announcements",
    "Yeni Duyuru Ekle": "Add New Announcement",
    "Henüz eklenmiş bir duyuru bulunmamaktadır.": "No announcement has been added yet.",
    "Bu duyuruyu silmek istediğinize emin misiniz?": "Are you sure you want to delete this announcement?",
    "Akademik Takvim": "Academic Calendar",
    "Faaliyet": "Activity",
    "Tarih": "Date",
    "2025-2026 Güz Yarıyılı": "2025-2026 Fall Semester",
    "Derslerin Başlaması": "Start of Classes",
    "Derslerin Sona Ermesi": "End of Classes",
    "2025-2026 Bahar Yarıyılı": "2025-2026 Spring Semester",
    "Ara Sınavlar (Vize)": "Midterm Exams",
    "Bahar Yarıyılı Ders Bitişi": "End of Spring Semester Classes",
    "Yarıyıl Sonu Sınavları (Final)": "Final Exams",
    "Ders Programı": "Course Schedule"
}

po_path = "app/translations/en/LC_MESSAGES/messages.po"
mo_path = "app/translations/en/LC_MESSAGES/messages.mo"

# 1. Read existing PO
with open(po_path, 'rb') as f:
    catalog = read_po(f)

# 2. Add new translations
for msgid, msgstr in translations.items():
    catalog.add(msgid, msgstr)

# 3. Write back to PO
with open(po_path, 'wb') as f:
    write_po(f, catalog)

# 4. Compile to MO
with open(mo_path, 'wb') as f:
    write_mo(f, catalog)

print("Translations successfully updated and compiled!")
