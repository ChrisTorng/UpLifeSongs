import subprocess

def run_command(command):
    """
    執行 shell 命令並返回輸出與錯誤信息
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

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
        run_command("git add .")
        commit_message = "Auto-sync changes"
        run_command(f'git commit -m "{commit_message}"')
        print("Changes committed.")

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