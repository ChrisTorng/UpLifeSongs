import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import demucs.separate

def run_demucs(fullpath):
    demucs.separate.main(["-n", "htdemucs_6s", "--mp3", "--mp3-bitrate", "128", fullpath])

def move_and_rename_files(current_dir, filename):
    prefix = os.path.splitext(filename)[0]
    separated_dir = os.path.join(current_dir, "separated", "htdemucs_6s", prefix)
    new_folder = os.path.join(current_dir, prefix)

    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
        print(f"{prefix} folder created.")

    # Move and rename the original MP3 file
    shutil.move(os.path.join(current_dir, filename), os.path.join(new_folder, "original.mp3"))
    print("original.mp3 moved.")

    # Move and rename separated files
    for separated_file in os.listdir(separated_dir):
        src_path = os.path.join(separated_dir, separated_file)
        dst_path = os.path.join(new_folder, separated_file)

        if separated_file == "drums.mp3":
            dst_path = os.path.join(new_folder, "drum.mp3")
        elif separated_file == "vocals.mp3":
            dst_path = os.path.join(new_folder, "vocal.mp3")

        shutil.move(src_path, dst_path)
        print(f"{os.path.basename(dst_path)} moved.")

    # Remove the empty separated folder
    shutil.rmtree(separated_dir)

def generate_waveform(mp3_path, png_path, size=(600, 30), dpi=96):
    audio = AudioSegment.from_mp3(mp3_path)
    samples = np.array(audio.get_array_of_samples())

    if audio.channels == 2:
        samples = samples[::2]

    samples = samples / (2**15)

    plt.figure(figsize=(size[0]/dpi, size[1]/dpi), dpi=dpi)
    plt.plot(samples, color='blue', linewidth=dpi/96)
    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.ylim(-1, 1)
    plt.savefig(png_path, format='png', transparent=True)
    plt.close()

def process_mp3(current_dir, filename):
    print(f"Processing {filename}...")
    
    # Step 1: Run Demucs
    fullpath = os.path.join(current_dir, filename)
    run_demucs(fullpath)
    print("Demucs processing completed.")

    # Step 2: Move and rename files
    move_and_rename_files(current_dir, filename)

    # Step 3: Generate waveforms
    new_folder = os.path.join(current_dir, os.path.splitext(filename)[0])
    for mp3_file in os.listdir(new_folder):
        if mp3_file.endswith('.mp3'):
            mp3_path = os.path.join(new_folder, mp3_file)
            png_path = os.path.join(new_folder, os.path.splitext(mp3_file)[0] + '.png')
            generate_waveform(mp3_path, png_path)
            print(f"Waveform generated for {mp3_file}")

    print(f"Processing completed for {filename}\n")

def main():
    current_dir = os.getcwd()
    
    for filename in os.listdir(current_dir):
        if filename.endswith('.mp3'):
            process_mp3(current_dir, filename)

if __name__ == '__main__':
    main()