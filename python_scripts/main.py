import json, re
from pathlib import Path
from typing import Union

from utils.embed_dialog_json import embed_dialog_into_event
from utils.add_file2lang_index import add_filename_to_language_indexes
from utils.stories_json2bilingual_dict import story_json2bilingual
from save_json2languages import save_bilingual_json

'''
对于每一行，提取如下变量，例如（就举个例子）

character_code	dialog_code	dialog_cn	dialog_en	face
char.father	startlog_1	不带把，不能要	No dick, this one is useless.	null

如果没有人物冒号，character_code留空

并转换成嵌套式json

{
  "startlog": {
    "1": {
      "character_code": "...",
      "dialog": { "cn": "...", "en": "..." },
      "face": "..."
    },
    ...
  }
}

'''

def build_nested_dialog_json(dialog_cn, dialog_en, output_file):

    with open(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\languages\zh\characters.json", \
              "r", encoding="utf-8") as f:
        char_map = json.load(f)

    reverse_char_map = {v: k for k, v in char_map.items()}

    # 构造嵌套式 JSON
    nested_output = {"log": {}}
    for i, (cn, en) in enumerate(zip(dialog_cn, dialog_en), 1):
        m = re.match(r"(.+?)[：:](.*)", cn)

        if m:
            speaker, line = m.groups()
            character_code = reverse_char_map.get(speaker.strip(), "")
            dialog_cn_clean = line.strip()
        else:
            character_code = ""
            dialog_cn_clean = cn.strip()
        nested_output["log"][str(i)] = {
            "character_code": character_code,
            "dialog": {
                "cn": dialog_cn_clean,
                "en": en.strip()
            },
            "face": "null"
        }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(nested_output, f, ensure_ascii=False, indent=2)


def check_event_exists(target_code: str, 
                       map_json_path: Union[str, Path]) -> None:
    """
    检查指定地图 JSON 中是否存在调用特定 text code 的事件（如 "TRASHCAN01"）。
    如果未找到，则抛出 ValueError。

    Parameters:
    - map_json_path: 地图 JSON 文件路径
    - target_code: 要查找的事件命令参数（如 Text Code）

    Raises:
    - FileNotFoundError: 如果 JSON 文件不存在
    - ValueError: 如果未找到任何匹配的事件命令参数
    """
    map_json_path = Path(map_json_path)
    if not map_json_path.exists():
        raise FileNotFoundError(f"❌ Map file not found: {map_json_path}")

    with open(map_json_path, "r", encoding="utf-8") as f:
        map_data = json.load(f)

    events = map_data.get("events", [])
    for event in events:
        if not event:
            continue
        for page in event.get("pages", []):
            for cmd in page.get("list", []):
                if cmd.get("code") == 118 and target_code in cmd.get("parameters", []):
                    return  # Found

    raise ValueError(f"❌ Text code '{target_code}' not found in any event of map '{map_json_path.name}'")


dialog_cn = [
    "*：这就是我重生到20年前的经历。",
    "*：虽然是20年前，但好歹我也是重生者啊。",
    "*：怎么这比上一世还惨。",
    "*：上一世我爹也没因为我不带把把我扔了。",
    "*：唉，果然这种事情也会发生的吧……",
    "*：这辈子有了。",
    "*：咦，这是什么。",
    "*：仙丹？",
    "系统：检测到你在抱怨，送你一颗仙丹。",
    "*：系统？仙丹？",
    "*：哇，果然天无绝人之路。"
]

dialog_en = [
    "So this is what it's like to be reborn 20 years in the past.",
    "Even if it’s 20 years ago, I’m a reincarnator, right?",
    "Why is this life even worse than the last one?",
    "At least in my last life, Dad didn’t throw me away just for being dickless.",
    "Sigh... This happens, though.",
    "This life is screwed.",
    "Huh? What’s this?",
    "An elixir?",
    "Complaint detected. Dispensing one elixir.",
    "System? Elixir?",
    "Whoa, guess god hasn’t abandoned me."
]

output_file, map_path = (
    Path(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\data\stories_json\TRASHCAN01.json"),
    Path(r"C:\Users\xinra\OneDrive\Documents\RMMZ\RebirthAbandon\data\Map004.json")
)

if __name__ == "__main__":

    # 将中英文对话列表合并为一个按序号索引的嵌套 JSON 文件，
    # 并标注说话人代码和表情信息，输出到output_file
    build_nested_dialog_json(dialog_cn, dialog_en, output_file)

    check_event_exists(Path(output_file).stem, map_path)

    # 从指定的对话 output_file.json 中读取内容，生成新的对话命令序列，
    # 并在地图 JSON 文件中查找与该对话名（即 code: 118 的 label，
    # 例如 TRASHCAN01）匹配的事件。在该 label 出现的位置后，函数会替换
    # 从 label 到最后一个对话命令（code: 401）之间的内容，插入新的对话段落。
    # 如果找不到匹配的 label，则抛出错误。
    embed_dialog_into_event(map_path, output_file)

    # 将指定的新文件名添加到所有语言目录中的 index.json，
    # 若已存在则跳过，避免重复。
    add_filename_to_language_indexes(Path(output_file).stem)

    # 将指定的剧情 JSON 文件中的中英文对话提取出来，
    # 按 {文件名: {"zh": {...}, "eng": {...}}} 格式构建成双语字典。
    results = story_json2bilingual(output_file)

    # 将双语字典按语言拆分，分别保存到指定目录下的 zh 和 eng 文件夹中。
    save_bilingual_json(results, base_dir=Path("../RebirthAbandon/languages"))

#git gc --prune=now