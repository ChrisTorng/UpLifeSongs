import os
import shutil

def process_files():
    current_dir = os.getcwd()
    separated_dir = os.path.join(current_dir, "separated", "htdemucs_6s")

    if not os.path.exists(separated_dir):
        print("The directory ./separated/htdemucs_6s does not exist.")
        return

    for file in os.listdir(current_dir):
        if file.endswith(".mp3"):
            prefix = os.path.splitext(file)[0]
            separated_folder = os.path.join(separated_dir, prefix)
            
            if os.path.exists(separated_folder):
                # Create new directory if it doesn't exist
                new_folder = os.path.join(current_dir, prefix)
                if not os.path.exists(new_folder):
                    os.mkdir(new_folder)
                    print(prefix + " created.")
                
                # Move and rename the MP3 file
                new_mp3_path = os.path.join(new_folder, "original.mp3")
                shutil.move(os.path.join(current_dir, file), new_mp3_path)
                print("original.mp3 moved.")

                # Move files from ./separated/htdemucs_6s/<ABC> to new directory
                for separated_file in os.listdir(separated_folder):
                    separated_file_path = os.path.join(separated_folder, separated_file)
                    target_path = os.path.join(new_folder, separated_file)

                    shutil.move(separated_file_path, target_path)
                    
                    # Rename specific files
                    if separated_file == "drums.mp3":
                        os.rename(target_path, os.path.join(new_folder, "drum.mp3"))
                        print("drum.mp3 moved.")
                    elif separated_file == "vocals.mp3":
                        os.rename(target_path, os.path.join(new_folder, "vocal.mp3"))
                        print("vocal.mp3 moved.")
                    else:
                        print(separated_file + " moved.")

if __name__ == '__main__':
    process_files()
