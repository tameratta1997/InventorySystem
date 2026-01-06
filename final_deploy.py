import os
import subprocess
import time

def deploy():
    # PATHs
    git_dir = os.path.abspath("mingit/cmd")
    git_exe = os.path.join(git_dir, "git.exe")
    os.environ["PATH"] = git_dir + os.pathsep + os.environ["PATH"]

    print(f"Using Git: {git_exe}")
    
    def run(cmd):
        print(f"EXEC: {' '.join(cmd)}")
        subprocess.run(cmd, check=False) # Don't crash on error, just continue

    # 1. Config
    run(["git", "config", "--global", "user.name", "tameratta1997"])
    run(["git", "config", "--global", "user.email", "tameratta1997@users.noreply.github.com"])
    
    # 2. Init
    if not os.path.exists(".git"):
        run(["git", "init"])
        run(["git", "branch", "-M", "main"])
    
    # 3. Commit
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial commit"])

    # 4. Check GH Auth
    gh_exe = r"C:\Program Files\GitHub CLI\gh.exe"
    
    # 5. Create and Push
    # We try to create. If it exists, we just push.
    print("creating repo...")
    # --source . will prompt to push. --push handles it.
    proc = subprocess.run([gh_exe, "repo", "create", "tameratta1997/InventorySystem", "--public", "--source=.", "--remote=origin", "--push"], capture_output=True, text=True)
    
    if proc.returncode != 0:
        print("GH output:", proc.stderr)
        if "already exists" in proc.stderr:
            print("Repo exists. Linking and pushing...")
            run(["git", "remote", "add", "origin", "https://github.com/tameratta1997/InventorySystem.git"])
            run(["git", "push", "-u", "origin", "main"])
    else:
        print("GH Success:", proc.stdout)

if __name__ == "__main__":
    deploy()
