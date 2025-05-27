import os
import json
from pathlib import Path
from typing import Dict

def save_bilingual_json(data: Dict[str, Dict[str, str]], base_dir: str = "languages"):
    """
    Save bilingual dictionaries into structured language folders like 'cn', 'eng'.

    Parameters:
    - data: Dict mapping logical file names (e.g., 'characters') to a dict with language codes (e.g., 'cn', 'eng').
    - base_dir: Base directory where language folders will be created.
    """
    for lang_code in {"zh", "eng"}:
        lang_folder = Path(base_dir) / lang_code
        lang_folder.mkdir(parents=True, exist_ok=True)
        for filename, lang_data in data.items():
            #print(f"Saving {lang_data} {lang_code}...")
            filepath = lang_folder / f"{filename}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(lang_data[lang_code], f, ensure_ascii=False, indent=2)

def import_json(file_path: str) -> Dict:
    """
    Import JSON data from a file.

    Parameters:
    - file_path: Path to the JSON file.

    Returns:
    - Dictionary containing the JSON data.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f) 

bilingual_data = {
  "START_LOG": {
    "zh": {
      "START_LOG01": "不带把，不能要。",
      "START_LOG02": "你……你太过分了。",
      "START_LOG03": "这已经是第三个不带把的了，还不都怪你？",
      "START_LOG04": "……",
      "START_LOG05": "我打工赚不了那么多钱。",
      "START_LOG06": "养那么多不带把的，以后家门被砸了都没个能给我出气的。",
      "START_LOG07": "哼。",
      "START_LOG08": "（抱起我出门）",
      "START_LOG09": "你，你放下她！",
      "START_LOG10": "少废话，不然我踹你。",
      "START_LOG11": "呜……呜呜呜……",
      "START_LOG12": "（就这样，我被自己的亲爹扔进了郊外的垃圾桶。）"
    },
    "eng": {
      "START_LOG01": "No dick, this one is useless.",
      "START_LOG02": "You... you've gone too far.",
      "START_LOG03": "This is already the third one without a dick. It's all your fault.",
      "START_LOG04": "...",
      "START_LOG05": "I can't earn that much money from my job.",
      "START_LOG06": "Raising so many without dicks—when someone comes to our door looking for trouble, who'll fight for me?",
      "START_LOG07": "Hmph.",
      "START_LOG08": "(Picks me up and walks out.)",
      "START_LOG09": "You, you put her down!",
      "START_LOG10": "Shut up or I'll kick you.",
      "START_LOG11": "Wuwu... sob sob sob...",
      "START_LOG12": "(And just like that, my own father threw me into a trash can in the suburbs.)"
    }
  }
}

#bilingual_data = ""

if __name__ == "__main__":

    base_path = Path("../RebirthAbandon/languages")

    if bilingual_data is str and os.path.exists(bilingual_data):
        bilingual_data = import_json(bilingual_data)

    save_bilingual_json(bilingual_data, base_dir=base_path)