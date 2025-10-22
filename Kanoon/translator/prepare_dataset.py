import json
import csv

def build_finetune_dataset(input_csv="data/law_articles.csv", output_jsonl="data/fine_tune_dataset.jsonl"):
    dataset = []

    with open(input_csv, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            article = row.get("Article/Section", "").strip()
            content = row.get("Description", "").strip()

            if not article or not content:
                continue

            entry = {
                "instruction": f"What is {article}?",
                "input": "",
                "output": f"{article}: {content}"
            }
            dataset.append(entry)

    # Save as JSONL
    with open(output_jsonl, "w", encoding="utf-8") as out_file:
        for item in dataset:
            out_file.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Dataset written to {output_jsonl} with {len(dataset)} entries.")

if __name__ == "__main__":
    build_finetune_dataset()
