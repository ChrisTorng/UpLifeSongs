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

    # Step 1: Sync with the remote branch
    print("Syncing with the remote branch...")
    output, error = run_command('git pull origin main --rebase')
    print("Pull output:", output)
    if error:
        print("Pull error:", error)
        if "conflict" in error.lower():
            print("Conflict detected. Please resolve conflicts manually and re-run the script.")
        return

    # Step 2: Stage changes
    print("Staging changes...")
    run_command('git add .')

    # Step 3: Commit changes
    print("Committing changes...")
    output, error = run_command(f'git commit -m "{commit_message}"')
    print("Commit output:", output)
    if error:
        print("Commit error:", error)

    # Step 4: Push changes
    print("Pushing changes to remote...")
    output, error = run_command('git push origin main')
    print("Push output:", output)
    if error:
        print("Push error:", error)

if __name__ == "__main__":
    main()
