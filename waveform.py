import os
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

def generate_waveform(mp3_path, png_path, size=(600, 30), dpi=96):
    # 讀取 MP3 檔案
    audio = AudioSegment.from_mp3(mp3_path)

    # 取得音訊的左聲道數據
    samples = np.array(audio.get_array_of_samples())

    # 如果為立體聲，僅取左聲道
    if audio.channels == 2:
        samples = samples[::2]

    # 正規化數據
    samples = samples / (2**15)

    # 創建波型圖
    plt.figure(figsize=(size[0]/dpi, size[1]/dpi), dpi=dpi)
    plt.plot(samples, color='blue', linewidth=dpi/96) # 使用藍色，線寬設為 DPI 的 1/30
    #plt.axhline(0, color='blue', linewidth=dpi/96) # 在 y=0 處添加一條藍色直線
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.ylim(-1, 1) # 限制 y 軸的範圍以確保直線可見
    plt.savefig(png_path, format='png', transparent=True)
    plt.close()

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.mp3'):
                mp3_path = os.path.join(root, filename)
                png_path = os.path.join(root, os.path.splitext(filename)[0] + '.png')

                # 檢查 PNG 檔案是否已存在
                if os.path.exists(png_path):
                    # print(f'{png_path} exists, skip.')
                    continue

                generate_waveform(mp3_path, png_path)
                print(f'{png_path[len(directory) + 1:]} generated.')

if __name__ == '__main__':
    # 使用當前 Python 檔所在的資料夾
    directory = os.path.dirname(os.path.realpath(__file__))
    process_directory(directory)
