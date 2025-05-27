import json
import shutil

with open("Tilesets.json", encoding="utf-8") as f:
    data = json.load(f)

outside_b = next((t for t in data if isinstance(t, dict) and t.get("name") == "Outside_B"), None)
sf_outside_b = next((t for t in data if isinstance(t, dict) and t.get("name") == "SF_Outside_B"), None)

if outside_b is None or sf_outside_b is None:
    raise ValueError("Could not find 'Outside_B' or 'SF_Outside_B' tileset in Tilesets.json")

# Rename original Tilesets.json to backup
original_path = "/mnt/data/Tilesets.json"
backup_path = "/mnt/data/Tilesets_backup.json"

shutil.copyfile(original_path, backup_path)

merged_tileset = sf_outside_b.copy()
merged_tileset["name"] = "Merged_Outside_B"
merged_tileset["tilesetNames"] = outside_b["tilesetNames"] + sf_outside_b["tilesetNames"]
merged_tileset["flags"] = outside_b["flags"] + sf_outside_b["flags"]
merged_tileset["terrainTags"] = outside_b["terrainTags"] + sf_outside_b["terrainTags"]

data.append(merged_tileset)

with open("Tilesets.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
