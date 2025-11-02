import json, csv, glob, os

json_files = glob.glob("*.json")

for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tworzymy CSV o tej samej nazwie
    csv_name = os.path.splitext(file)[0] + ".csv"
    with open(csv_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Price", "Description", "Image URL"])

        for p in data:
            writer.writerow([
                p.get("nazwa", ""),
                p.get("cena", ""),
                p.get("opis", ""),
                p.get("zdjecie", "")
            ])

    print(f"Zapisano: {csv_name}")
