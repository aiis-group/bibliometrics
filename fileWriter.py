import json
import sys



def writeJSON(data):
    with open('result.json', 'w', encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False)
