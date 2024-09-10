import json
import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

def main():
    # Read the JSON file
    with open('songsList.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Get the first group
    first_group = data['groups'][0]
    sub_title = first_group['subTitle']

    # Prepare the commit message
    commit_message = f"Add {sub_title} songs."

    # Wait for user input
    input(f"Press Enter to git add/commit \"{commit_message}\"...")

    # Git add
    run_command('git add .')

    # Git commit
    output, error = run_command(f'git commit -m "{commit_message}"')
    print("Commit output:", output)
    if error:
        print("Commit error:", error)

    # Wait for user input
    input("Press Enter to push changes...")

    # Git push
    output, error = run_command('git push')
    print("Push output:", output)
    if error:
        print("Push error:", error)

if __name__ == "__main__":
    main()