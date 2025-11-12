import json
import csv

# Pliki
INPUT_JSON = "kategorie.json"
OUTPUT_CSV = "kategorie.csv"

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    categories = json.load(f)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    
    # Nagłówki zgodne z PrestaShop
    writer.writerow(["Name", "Parent category", "Active"])
    
    for cat in categories:
        writer.writerow([cat, "Produkty", 1])

print(f"✅ Zapisano CSV do: {OUTPUT_CSV}")
