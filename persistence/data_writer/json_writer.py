import json

def store_researchers(researchers):
    with open('results/researchers.json', 'w', encoding="utf-8") as fp:
        json.dump([r.to_dict() for r in researchers], fp, ensure_ascii=False)