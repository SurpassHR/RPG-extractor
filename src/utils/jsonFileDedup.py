import json

# 读取JSON文件
with open("...", 'r', encoding='utf-8') as f:
    data = json.load(f)  # json.load会自动处理重复键，保留最后一个

# 重新写入文件（已去重）
with open("...", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)