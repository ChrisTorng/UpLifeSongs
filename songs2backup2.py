import json
import os

# 定義來源與目標檔案路徑
source_file = "songsList.json"
target_file = "../UpLifeSongsBackup2/songsList.json"

# 讀取 JSON 檔案
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 儲存 JSON 檔案
def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 合併「其他」的 songs，避免重複並保持單一「其他」項目
def merge_others_songs(source_groups, target_groups):
    source_others = next((g for g in source_groups if g["subTitle"] == "其他"), None)
    target_others = next((g for g in target_groups if g["subTitle"] == "其他"), None)

    if source_others:
        if target_others:
            # 若目標已經有「其他」，合併來源的「其他」 songs，並排除重複
            new_songs = [song for song in source_others["songs"] if song not in target_others["songs"]]
            target_others["songs"].extend(new_songs)
        else:
            # 若目標沒有「其他」，直接加入來源的「其他」
            target_groups.append(source_others)

# 載入來源和目標的 JSON 資料
source_data = load_json(source_file)
target_data = load_json(target_file)

# 移動來源的 groups 到目標的 groups 前方
target_data["groups"] = source_data["groups"] + target_data["groups"]

# 合併「其他」的 songs，避免重複並保持單一「其他」項目
merge_others_songs(source_data["groups"], target_data["groups"])

# 移除來源的所有 groups 內容
source_data["groups"] = []

# 儲存更新後的 JSON 檔案
save_json(source_file, source_data)  # 更新來源檔案以清空 groups
save_json(target_file, target_data)  # 更新目標檔案以合併資料

print("搬移與合併完成！")
