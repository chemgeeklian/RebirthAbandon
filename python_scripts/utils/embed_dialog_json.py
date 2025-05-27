import json
from pathlib import Path

def embed_dialog_into_event(map_path, dialog_json_path):
    """
    替换 RPG Maker 地图事件中指定 label（118 code）后的内容，
    直到最后一个 401 对话命令为止，用新的对话块替代。
    """
    map_path = Path(map_path)
    dialog_json_path = Path(dialog_json_path)
    label_name = dialog_json_path.stem  # e.g., "TRASHCAN01"

    with open(map_path, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    with open(dialog_json_path, "r", encoding="utf-8") as f:
        dialog_data = json.load(f)

    dialog_entries = dialog_data.get("log", {})
    dialog_block = []

    # 生成新的对话 block
    for key in sorted(dialog_entries.keys(), key=lambda x: int(x)):
        entry = dialog_entries[key]
        char_name = entry.get("character_code", "")
        dialog_code = f"{label_name}{int(key):02d}"
        dialog_block.append({
            "code": 101,
            "indent": 0,
            "parameters": ["", 0, 0, 2, f"${{{char_name}}}" if char_name else ""]
        })
        dialog_block.append({
            "code": 401,
            "indent": 0,
            "parameters": [f"${{{dialog_code}}}"]
        })

    # 在 events 中查找包含指定 label 的事件
    for event in map_data.get("events", []):
        if not event:
            continue
        for page in event.get("pages", []):
            cmd_list = page.get("list", [])
            label_idx = None
            last_401_idx = None

            # Step 1: 找到 label（code 118）
            for i, cmd in enumerate(cmd_list):
                if cmd.get("code") == 118 and cmd.get("parameters", [None])[0] == label_name:
                    label_idx = i
                    continue
                if label_idx is not None and cmd.get("code") == 401:
                    last_401_idx = i

            if label_idx is not None:
                insert_start = label_idx + 1
                insert_end = (last_401_idx + 1) if last_401_idx is not None else insert_start

                # 替换指定段落
                page["list"] = cmd_list[:insert_start] + dialog_block + cmd_list[insert_end:]
                break
        else:
            continue  # 当前 event 不包含 label，尝试下一个
        break
    else:
        raise ValueError(f"❌ 未在 {map_path.name} 中找到 label '{label_name}'")

    # 保存修改后的 map 文件
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {Path(dialog_json_path).stem} 剧情成功嵌入 {Path(map_path).name}")


# 调用示例
if __name__ == "__main__":

    # 配置路径
    dialog_json_path = Path(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\data\stories_json\START_LOG.json")
    map_path = Path(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\data\Map003.json")

    #add_filename_to_language_indexes(Path(dialog_json_path).stem)
    embed_dialog_into_event(map_path, dialog_json_path)