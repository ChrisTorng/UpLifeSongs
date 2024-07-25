import sys
import os
from yt_dlp import YoutubeDL

class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(f"錯誤: {msg}")

def my_hook(d):
    if d['status'] == 'finished':
        print(f"開始轉換: {d['filename']}")

def download_mp3(urls):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': {
            'default': '%(title)s.%(ext)s'
        },
        'prefer_ffmpeg': True,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'quiet': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                info = ydl.extract_info(url, download=False)
                title = info['title']
                print(f"開始下載: {title}")
                ydl.download([url])
            except Exception as e:
                print(f'下載失敗: {url}')
                print(f'錯誤: {str(e)}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python yt2mp3.py [YouTube URL1] [YouTube URL2] ...")
    else:
        download_mp3(sys.argv[1:])