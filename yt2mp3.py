import sys
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

def download_mp3(url, custom_filename=None):
    if not url.startswith('http'):
        url = f'https://www.youtube.com/watch?v={url}'

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yt2mp3.py [YouTube URL or ID] [Optional: Custom filename]")
    elif len(sys.argv) == 2:
        download_mp3(sys.argv[1])
    else:
        download_mp3(sys.argv[1], sys.argv[2])