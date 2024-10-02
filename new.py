import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from yt_dlp import YoutubeDL

def get_next_sunday(today=None):
    if today is None:
        today = datetime.today()
    days_ahead = 6 - today.weekday()  # 星期日是6
    if days_ahead <= 0:
        days_ahead += 7
    next_sunday = today + timedelta(days=days_ahead)
    # 使用 f-string 格式化，避免前導零
    return f"{next_sunday.year}/{next_sunday.month}/{next_sunday.day}"

def extract_video_id(url):
    """
    從 YouTube URL 中提取視頻 ID。
    支援多種 URL 格式。
    """
    regex = (r'(?:v=|\/)([0-9A-Za-z_-]{11}).*')
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_info(url):
    """
    使用 yt_dlp 獲取視頻資訊，包括標題和視頻 ID。
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id')
            title = info.get('title')
            return video_id, title
        except Exception as e:
            print(f"錯誤: 無法獲取 URL '{url}' 的資訊。錯誤訊息: {e}")
            return None, None

def load_json(file_path):
    if not os.path.exists(file_path):
        print(f"錯誤: 檔案 {file_path} 不存在。")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"已成功更新 {file_path}。")

def main():
    parser = argparse.ArgumentParser(description='新增 YouTube 影片至 songsList.json。')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='YouTube 影片的 URL')
    args = parser.parse_args()

    # 取得目前腳本的絕對路徑
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'songsList.json')

    # 計算下一個週日的日期
    next_sunday = get_next_sunday()

    # 載入 songsList.json
    data = load_json(json_path)

    # 查找是否已存在下一個週日的 group
    groups = data.get('groups', [])
    group = next((g for g in groups if g.get('subTitle') == next_sunday), None)

    if group:
        print(f"找到已存在的 group: {next_sunday}")
    else:
        print(f"未找到 group: {next_sunday}，將建立新的 group。")
        group = {
            "subTitle": next_sunday,
            "subTitleUrl": "",
            "songs": []
        }
        # 將新 group 插入到最前面
        groups.insert(0, group)

    # 處理每個 YouTube URL
    for url in args.urls:
        video_id, title = get_video_info(url)
        if not video_id or not title:
            print(f"警告: 無法從 URL '{url}' 中提取視頻 ID 或標題，將跳過此 URL。")
            continue
        # 檢查是否已存在相同的 youtubeId
        if any(song.get('youtubeId') == video_id for song in group['songs']):
            print(f"警告: youtubeId '{video_id}' 已存在於 group '{next_sunday}'，將跳過。")
            continue
        song_entry = {
            "name": title,
            "youtubeId": video_id
        }
        group['songs'].append(song_entry)
        print(f"新增歌曲: {title} (ID: {video_id})")

    # 更新 JSON 結構
    data['groups'] = groups

    # 保存回 songsList.json
    save_json(data, json_path)

if __name__ == "__main__":
    main()
