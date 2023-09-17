import os
import shutil

# Iterate over all .mp3 files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.mp3'):
        # Extract filename without extension
        name_without_extension = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        # Tokenize the filename based on '_'
        tokens = name_without_extension.split('_')

        # Check the number of tokens to decide the action
        if len(tokens) >= 2:
            if len(tokens) == 2:
                foldername = tokens[0]
            else:
                foldername = tokens[1]

            instrument = tokens[-1]  # The last token is considered as instrument

            # Remove leading and trailing characters
            instrument = instrument[1:-1]

            # Convert to lowercase
            instrument = instrument.lower()

            # Replace specific words
            instrument = instrument.replace('drums', 'drum')
            instrument = instrument.replace('vocals', 'vocal')

            new_filename = f"{instrument}{extension}"
        else:
            foldername = name_without_extension
            new_filename = 'original.mp3'

        # Create directory if it doesn't exist
        if not os.path.exists(foldername):
            os.makedirs(foldername)

        # Move the file to the new directory
        new_fullname = os.path.join(foldername, new_filename)
        shutil.move(filename, new_fullname)
        print(f'{new_fullname} moved.')
