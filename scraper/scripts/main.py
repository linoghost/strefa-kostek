import os
import json
import csv
import html

# 🔧 Ustawienia
DATA_DIR = os.path.join("..", "scraper_data")
OUTPUT_DIR = os.path.join("..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "produkty.csv")

# Separator wielu zdjęć
MULTI_IMAGE_SEPARATOR = ", "
# Separator pól CSV (w PL często używa się średnika)
CSV_DELIMITER = ";"
# Limit produktów (None = bez limitu)
LIMIT = None

# Kolumny CSV zgodne z PrestaShop
CSV_FIELDS = ["kategoria", "nazwa", "cena", "opis", "zdjecia"]

produkty = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".json"):
        json_path = os.path.join(DATA_DIR, file)
        kategoria = os.path.splitext(file)[0]

        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Błąd w pliku: {file}")
                continue

        for produkt in data:
            if isinstance(produkt, dict):
                produkt["kategoria"] = kategoria

                # 🖼️ Zbierz wszystkie zdjęcia z kluczy zaczynających się od "zdjecie"
                images = []
                for key, value in produkt.items():
                    if key.startswith("zdjecie") and isinstance(value, str) and value.startswith("https"):
                        images.append(value)
                produkt["zdjecia"] = MULTI_IMAGE_SEPARATOR.join(images)

                # ✨ Dekodowanie encji HTML → polskie znaki
                for key, val in produkt.items():
                    if isinstance(val, str):
                        produkt[key] = html.unescape(val)

                produkty.append({
                    "kategoria": produkt["kategoria"],
                    "nazwa": produkt.get("nazwa", ""),
                    "cena": produkt.get("cena", ""),
                    "opis": produkt.get("opis", ""),
                    "zdjecia": produkt["zdjecia"]
                })

                if LIMIT is not None and len(produkty) >= LIMIT:
                    break
        if LIMIT is not None and len(produkty) >= LIMIT:
            break

# 💾 Zapis CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS, delimiter=CSV_DELIMITER)
    writer.writeheader()
    writer.writerows(produkty)

print(f"✅ Zapisano {len(produkty)} produktów do pliku: {OUTPUT_CSV}")
