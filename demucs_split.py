import os
import demucs.separate

def run_demucs():
    current_directory = os.getcwd()
    
    for filename in os.listdir(current_directory):
        if filename.endswith('.mp3'):
            fullpath = os.path.join(current_directory, filename)
            demucs.separate.main(["-n", "htdemucs_6s", "--mp3", "--mp3-bitrate", "128", fullpath])

if __name__ == '__main__':
    run_demucs()
