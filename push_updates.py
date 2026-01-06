import os
import subprocess

def push_updates():
    # Setup Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    git_dir = os.path.join(base_dir, "mingit", "cmd")
    git_exe = os.path.join(git_dir, "git.exe")
    os.environ["PATH"] = git_dir + os.pathsep + os.environ["PATH"]

    if not os.path.exists(git_exe):
        print("Error: MinGit not found. Please re-run the installation step if needed.")
        return

    print(f"Using Git: {git_exe}")
    
    def run(cmd):
        print(f"EXEC: {' '.join(cmd)}")
        subprocess.run(cmd, check=False)

    # 1. Add all changes
    run(["git", "add", "."])
    
    # 2. Commit
    # We use 'subprocess.run' directly to catch the specific exit code if needed, 
    # but check=False is fine, it just won't crash if nothing to commit.
    print("EXEC: git commit")
    subprocess.run(["git", "commit", "-m", "Manual update request"], check=False)

    # 3. Push
    print("EXEC: git push origin main")
    subprocess.run(["git", "push", "-u", "origin", "main"], check=False)
    print("Done.")

if __name__ == "__main__":
    push_updates()
