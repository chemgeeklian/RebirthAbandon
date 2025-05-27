from pathlib import Path
import json

def add_filename_to_language_indexes(new_filename: str):
    """
    将指定的新文件名添加到每个语言目录中的 index.json 里，避免重复。
    """
    base_languages_dir = Path(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\languages")

    for lang_dir in base_languages_dir.iterdir():
        if not lang_dir.is_dir():
            continue

        index_file = lang_dir / "index.json"

        # 如果 index.json 不存在，初始化为空结构
        if index_file.exists():
            with open(index_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"files": []}

        # 添加新文件名（如不存在）
        if new_filename not in data["files"]:
            data["files"].append(new_filename)
            data["files"].sort()
            with open(index_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

# 仅当作为主程序运行时才调用
if __name__ == "__main__":
    filename = "START_LOG"
    add_filename_to_language_indexes(filename)
