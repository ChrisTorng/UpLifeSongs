import json
import subprocess

def run_command(command):
    """
    執行 shell 命令並返回輸出與錯誤信息
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('big5'), error.decode('big5')

def git_sync():
    """
    自動同步本地與遠端分支，包含提交、拉取和推送
    """
    # 檢查 Git 狀態
    print("Checking Git status...")
    output, error = run_command("git status --porcelain")
    if error:
        print(f"Error checking status: {error}")
        return

    # 如果有未提交的更改，自動提交
    if output.strip():
        print("Changes detected. Staging and committing...")

        # Read the JSON file
        with open('songsList.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Get the first group
        first_group = data['groups'][0]
        sub_title = first_group['subTitle']

        # Prepare the commit message
        commit_message = f"Add {sub_title} songs."

        # Wait for user input
        input(f"Press Enter to git add/commit/push \"{commit_message}\"...")

        run_command("git add .")

        # Git commit
        output, error = run_command(f'git commit -m "{commit_message}"')
        print("Commit output:", output)
        if error:
            print("Commit error:", error)

    # 拉取遠端更改
    print("Pulling remote changes...")
    output, error = run_command("git pull origin main --rebase")
    if error:
        print(f"Error during pull: {error}")
        if "conflict" in error.lower():
            print("Conflict detected. Please resolve conflicts manually.")
            return

    # 推送本地更改
    print("Pushing local changes to remote...")
    output, error = run_command("git push origin main")
    if error:
        print(f"Error during push: {error}")
    else:
        print("Sync completed successfully!")

if __name__ == "__main__":
    git_sync()