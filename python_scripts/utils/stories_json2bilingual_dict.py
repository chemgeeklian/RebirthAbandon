import json
from pathlib import Path

def story_json2bilingual(input_json_path: Path) -> dict:
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stem = input_json_path.stem
    bilingual_data = {stem: {"zh": {}, "eng": {}}}

    for key, entry in sorted(data.get("log", {}).items(), key=lambda x: int(x[0])):
        dialog_id = f"{stem}{int(key):02d}"
        bilingual_data[stem]["zh"][dialog_id] = entry["dialog"]["cn"]
        bilingual_data[stem]["eng"][dialog_id] = entry["dialog"]["en"]

    return bilingual_data

# 示例用法
if __name__ == "__main__":
    input_path = Path(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\data\stories_json\START_LOG.json")
    result = story_json2bilingual(input_path)
    #print(json.dumps(result, ensure_ascii=False, indent=2))
