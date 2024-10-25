import os
import shutil

# 定義來源和目標資料夾
source_dir = "."
target_dir = "../UpLifeSongsBackup"

# 確保目標資料夾存在
os.makedirs(target_dir, exist_ok=True)

# 獲取來源資料夾下的所有子資料夾名稱
for folder_name in os.listdir(source_dir):
    source_folder = os.path.join(source_dir, folder_name)
    target_folder = os.path.join(target_dir, folder_name)

    # 只處理子資料夾，並忽略名稱為 "separated" 的資料夾
    if os.path.isdir(source_folder) and folder_name != "separated":
        # 若目標資料夾下已有同名資料夾，則跳過
        if os.path.exists(target_folder):
            print(f"子資料夾 '{folder_name}' 已存在於目標資料夾中，跳過搬動。")
        else:
            # 搬移子資料夾到目標資料夾
            shutil.move(source_folder, target_folder)
            print(f"已搬動子資料夾 '{folder_name}' 到目標資料夾。")

# 刪除來源與目標資料夾中名為 "separated" 的資料夾（若存在）
for dir_path in [source_dir, target_dir]:
    separated_folder = os.path.join(dir_path, "separated")
    if os.path.isdir(separated_folder):
        shutil.rmtree(separated_folder)
        print(f"已刪除 '{dir_path}' 中的 'separated' 資料夾。")
