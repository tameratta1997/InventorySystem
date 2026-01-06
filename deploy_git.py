import os
import subprocess
import shutil

def find_git():
    # Common paths
    paths = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Users\Temo\AppData\Local\Programs\Git\cmd\git.exe",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return shutil.which("git")

def run_git(git_exe, args):
    cmd = [git_exe] + args
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=False)

def main():
    git_exe = find_git()
    if not git_exe:
        print("Git not found! Please check installation.")
        return

    print(f"Found Git at: {git_exe}")
    
    # Config
    run_git(git_exe, ["config", "--global", "user.name", "tameratta1997"])
    run_git(git_exe, ["config", "--global", "user.email", "tameratta1997@users.noreply.github.com"])
    
    # Init
    if not os.path.exists(".git"):
        run_git(git_exe, ["init"])
        # Rename branch to main
        run_git(git_exe, ["branch", "-M", "main"])

    # Add & Commit
    run_git(git_exe, ["add", "."])
    run_git(git_exe, ["commit", "-m", "Initial commit of Inventory System"])

    # Push using gh cli (it handles auth better)
    # But we need to add path to environment for gh to see git usually... 
    # Let's try adding to PATH for this process
    os.environ["PATH"] += os.pathsep + os.path.dirname(git_exe)
    
    # Create repo
    gh_exe = r"C:\Program Files\GitHub CLI\gh.exe"
    repo_cmd = [gh_exe, "repo", "create", "tameratta1997/InventorySystem", "--private", "--source=.", "--remote=origin", "--push"]
    
    print(f"Running GH: {' '.join(repo_cmd)}")
    subprocess.run(repo_cmd)

if __name__ == "__main__":
    main()
