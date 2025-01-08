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

def get_playlist_videos(playlist_url):
    """
    使用 yt_dlp 獲取播放清單中的所有影片資訊。
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
    }
    videos = []
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    video_id = entry.get('id')
                    title = entry.get('title')
                    if video_id and title:
                        videos.append({'id': video_id, 'title': title})
            return videos
        except Exception as e:
            print(f"錯誤: 無法獲取播放清單 '{playlist_url}' 的資訊。錯誤訊息: {e}")
            return []

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

def find_existing_song_name(youtube_id, current_file_path):
    """
    在當前和備份檔案中尋找相同 youtubeId 的歌曲名稱
    回傳: (歌名, 來源檔案路徑, 來源資料夾名稱, 來源日期) 或 (None, None, None, None)
    """
    paths = [
        current_file_path,
        "D:\\Projects\\GitHub\\ChrisTorng\\UpLifeSongsBackup2\\songsList.json",
        "D:\\Projects\\GitHub\\ChrisTorng\\UpLifeSongsBackup\\songsList.json"
    ]

    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for group in data.get('groups', []):
                    for song in group.get('songs', []):
                        if song.get('youtubeId') == youtube_id:
                            folder_name = os.path.basename(os.path.dirname(path))
                            return song.get('name'), path, folder_name, group.get('subTitle')
        except Exception as e:
            print(f"警告: 讀取 {path} 時發生錯誤: {e}")
    return None, None, None, None

def copy_song_folder(song_name, source_path, current_path):
    """
    複製歌曲資料夾從來源目錄到當前目錄
    """
    if source_path == current_path:
        return  # 如果是當前目錄找到的，不需要複製

    source_dir = os.path.dirname(source_path)
    target_dir = os.path.dirname(current_path)
    
    source_folder = os.path.join(source_dir, song_name)
    target_folder = os.path.join(target_dir, song_name)

    if os.path.exists(source_folder) and not os.path.exists(target_folder):
        try:
            import shutil
            shutil.copytree(source_folder, target_folder)
            print(f"已複製資料夾: {source_folder} -> {target_folder}")
        except Exception as e:
            print(f"警告: 複製資料夾失敗: {e}")

def main():
    parser = argparse.ArgumentParser(description='新增 YouTube 影片或播放清單至 songsList.json。')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='YouTube 影片或播放清單的 URL')
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
        if "playlist" in url:  # 檢測是否為播放清單
            print(f"檢測到播放清單 URL: {url}")
            videos = get_playlist_videos(url)
            for video in videos:
                video_id = video['id']
                if any(song.get('youtubeId') == video_id for song in group['songs']):
                    print(f"警告: youtubeId '{video_id}' 已存在於 group '{next_sunday}'，將跳過。")
                    continue
                
                # 尋找既有的歌名和來源
                existing_name, source_path, source_folder, source_date = find_existing_song_name(video_id, json_path)
                song_name = existing_name if existing_name else video['title']
                
                if existing_name and source_path:
                    copy_song_folder(existing_name, source_path, json_path)
                    print(f"複製自 {source_folder} 的 {source_date}")

                song_entry = {
                    "name": song_name,
                    "youtubeId": video_id
                }
                group['songs'].append(song_entry)
                print(f"新增播放清單影片: {song_name} (ID: {video_id})")
        else:
            video_id, title = get_video_info(url)
            if not video_id or not title:
                print(f"警告: 無法從 URL '{url}' 中提取視頻 ID 或標題，將跳過此 URL。")
                continue

            if any(song.get('youtubeId') == video_id for song in group['songs']):
                print(f"警告: youtubeId '{video_id}' 已存在於 group '{next_sunday}'，將跳過。")
                continue

            # 尋找既有的歌名和來源
            existing_name, source_path, source_folder, source_date = find_existing_song_name(video_id, json_path)
            song_name = existing_name if existing_name else title
            
            if existing_name and source_path:
                copy_song_folder(existing_name, source_path, json_path)
                print(f"複製自 {source_folder} 的 {source_date}")

            song_entry = {
                "name": song_name,
                "youtubeId": video_id
            }
            group['songs'].append(song_entry)
            print(f"新增歌曲: {song_name} (ID: {video_id})")

    # 更新 JSON 結構
    data['groups'] = groups

    # 保存回 songsList.json
    save_json(data, json_path)

if __name__ == "__main__":
    main()
