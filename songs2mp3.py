import json
import os
from yt_dlp import YoutubeDL

class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(f"Error: {msg}")

def my_hook(d):
    if d['status'] == 'finished':
        print(f"Starting conversion: {d['filename']}")

def download_mp3(youtube_id, custom_filename=None):
    url = f'https://www.youtube.com/watch?v={youtube_id}' if not youtube_id.startswith('http') else youtube_id

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': {
            'default': '%(title)s.%(ext)s' if not custom_filename else f'{custom_filename}.%(ext)s'
        },
        'prefer_ffmpeg': True,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'quiet': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            title = custom_filename or info['title']
            print(f"Starting download: {title}")
            ydl.download([url])
        except Exception as e:
            print(f'Download failed: {url}')
            print(f'Error: {str(e)}')

def load_songs_list():
    with open('songsList.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['groups'][0]['songs']

def download_song(youtube_id, name):
    if os.path.exists(f"{name}.mp3"):
        print(f"File '{name}.mp3' already exists. Skipping download.")
        return
    download_mp3(youtube_id, name)

def main():
    songs = load_songs_list()
    for song in songs:
        youtube_id = song['youtubeId']
        name = song['name']
        download_song(youtube_id, name)

if __name__ == "__main__":
    main()
