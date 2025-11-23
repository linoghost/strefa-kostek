import json
import csv
import os
import re

# Ścieżki
KATEGORIE_FILE = "kategorie.json"
PODKATEGORIE_DIR = "podkategorie"
OUTPUT_CSV = "kategorie_presta.csv"

def slugify(name):
    """
    Tworzy link_rewrite: małe litery, polskie znaki zamienione, spacje → myślniki
    """
    name = name.lower()
    # zamiana polskich znaków
    trans = str.maketrans("ąćęłńóśżź", "acelnoszz")
    name = name.translate(trans)
    # zamiana spacji i znaków specjalnych na '-'
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name

rows = []

# 1️⃣ Dodaj kategorię nadrzędną "Produkty"
rows.append({
    "Name": "Produkty",
    "Parent": "",
    "Active": 1,
    "Link_rewrite": slugify("Produkty"),
    "Meta_title": "Produkty",
    "Meta_keywords": "Produkty",
    "Meta_description": "Produkty"
})

# 2️⃣ Dodaj główne kategorie z kategorie.json pod "Produkty"
with open(KATEGORIE_FILE, "r", encoding="utf-8") as f:
    main_categories = json.load(f)

for cat in main_categories:
    rows.append({
        "Name": cat,
        "Parent": "Produkty",
        "Active": 1,
        "Link_rewrite": slugify(cat),
        "Meta_title": cat,
        "Meta_keywords": cat,
        "Meta_description": cat
    })

# 3️⃣ Dodaj podkategorie z plików
for filename in os.listdir(PODKATEGORIE_DIR):
    if filename.endswith(".json"):
        path = os.path.join(PODKATEGORIE_DIR, filename)

        # np. "Układanki-Klotski.json" → parent_name = "Układanki"
        parent_name = filename.split("_")[0]

        with open(path, "r", encoding="utf-8") as f:
            subcategories = json.load(f)

        for sub in subcategories:
            rows.append({
                "Name": sub,
                "Parent": parent_name,
                "Active": 1,
                "Link_rewrite": slugify(sub),
                "Meta_title": sub,
                "Meta_keywords": sub,
                "Meta_description": sub
            })

# 4️⃣ Zapisz do CSV dla Presty
with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as csvfile:
    fieldnames = ["Name", "Parent", "Active", "Link_rewrite", "Meta_title", "Meta_keywords", "Meta_description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Zapisano {len(rows)} rekordów do {OUTPUT_CSV}")
