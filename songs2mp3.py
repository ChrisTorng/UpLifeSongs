import json
import subprocess
import os

def load_songs_list():
    with open('songsList.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['groups'][0]['songs']

def download_song(youtube_id, name):
    # 檢查資料夾是否已存在
    if os.path.exists(name):
        print(f"Folder '{name}' already exists. Skipping download.")
        return

    command = ['python', 'yt2mp3.py', youtube_id, name]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully downloaded: {name}")
    except subprocess.CalledProcessError:
        print(f"Failed to download: {name}")

def main():
    songs = load_songs_list()
    for song in songs:
        youtube_id = song['youtubeId']
        name = song['name']
        download_song(youtube_id, name)

if __name__ == "__main__":
    main()