import os
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import write_mo

translations = {
    "Sınav Takvimi": "Exam Schedule",
    "2025-2026 EĞİTİM ÖĞRETİM YILI BAHAR DÖNEMİ BİLİŞİM GÜVENLİĞİ FİNAL SINAV PROGRAMI": "2025-2026 ACADEMIC YEAR SPRING SEMESTER INFORMATION SECURITY FINAL EXAM SCHEDULE",
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

print("Exam schedule translations successfully updated and compiled!")
