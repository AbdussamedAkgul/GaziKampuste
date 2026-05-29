import os
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import write_mo

translations = {
    "Arama Sonuçları": "Search Results",
    "İçin Arama Sonuçları": "Search Results For",
    "İlgili Sayfalar": "Related Pages",
    "Duyurular": "Announcements",
    "Yazar:": "Author:",
    "Eşleşen duyuru bulunamadı.": "No matching announcement found.",
    "Yemek Menüleri": "Cafeteria Menus",
    "Menüsü": "Menu",
    "Çorba:": "Soup:",
    "Ana Yemek:": "Main Dish:",
    "Yan Lezzet:": "Side Dish:",
    "Eşleşen menü bulunamadı.": "No matching menu found."
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

print("Search page translations successfully updated and compiled!")
