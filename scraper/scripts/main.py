import os
import json
import csv

# Ścieżki
DATA_DIR = os.path.join("..", "scraper_data")  # folder ze scraper_data
OUTPUT_DIR = os.path.join("..", "output")      # folder na gotowy CSV
os.makedirs(OUTPUT_DIR, exist_ok=True)         # tworzy folder jeśli nie istnieje
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "produkty.csv")

# Kolumny CSV (dostosowane do PrestaShop)
CSV_FIELDS = ["kategoria","nazwa","cena","opis",
              "zdjecie","zdjecie2","zdjecie3",
              "zdjecie_jpg","zdjecie2_jpg","zdjecie3_jpg"
            ]

produkty = []

# Przechodzimy przez wszystkie pliki JSON
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

        # Przetwarzamy każdy element
        for produkt in data:
            if isinstance(produkt, dict):
                produkt["kategoria"] = kategoria

                # Uzupełniamy brakujące zdjęcia pustymi stringami, żeby CSV było spójne
                for col in ["zdjecie", "zdjecie2", "zdjecie3",
                            "zdjecie_jpg", "zdjecie2_jpg", "zdjecie3_jpg"]:
                    if col not in produkt:
                        produkt[col] = ""

                produkty.append(produkt)
            else:
                print(f"❌ Pomijam element, bo nie jest słownikiem w pliku {file}: {produkt}")

# Zapis do CSV (nadpisuje przy każdym uruchomieniu)
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
    writer.writeheader()
    writer.writerows(produkty)

print(f"✅ Zapisano {len(produkty)} produktów do pliku: {OUTPUT_CSV}")
