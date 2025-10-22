# scripts/convert_csv_to_json.py

import csv
import json

csv_path = "data/law_articles.csv"
json_path = "data/legal_articles.json"

data = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title = row.get("Article/Section") or row.get("title") or row.get("Title")
        content = row.get("Description") or row.get("content") or row.get("Content")
        if title and content:
            data.append({"title": title.strip(), "content": content.strip()})

with open(json_path, "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, indent=2, ensure_ascii=False)

print(f"✅ Converted {len(data)} articles to JSON.")
