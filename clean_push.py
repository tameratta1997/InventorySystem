import os
import shutil
import subprocess
import time

def clean_and_push():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Prepare external git location
    src_dist = os.path.join(base_dir, "mingit_dist")
    temp_dist = os.path.join(os.environ["TEMP"], "mingit_dist_final")
    
    if os.path.exists(src_dist):
        if os.path.exists(temp_dist):
            shutil.rmtree(temp_dist)
        # Move it out of repo
        shutil.move(src_dist, temp_dist)
    elif not os.path.exists(temp_dist):
        print("Error: MinGit not found in repo or temp.")
        return

    # Setup Paths
    mingit_cmd = os.path.join(temp_dist, "cmd")
    mingit_bin = os.path.join(temp_dist, "mingw64", "bin")
    git_exe = os.path.join(mingit_cmd, "git.exe")
    
    env = os.environ.copy()
    env["PATH"] = mingit_bin + os.pathsep + env["PATH"]
    
    print(f"Using Git from: {git_exe}")
    
    # 2. Update .gitignore
    gitignore = os.path.join(base_dir, ".gitignore")
    with open(gitignore, "a") as f:
        f.write("\nmingit/\nmingit_dist/\n*.zip\nreinstall_git.py\nforce_push.py\nclean_push.py\n")
        
    def run(args):
        print(f"EXEC: {' '.join(args)}")
        subprocess.run([git_exe] + args, env=env, check=False)

    # 3. Fix Repo State
    # Stop tracking the binary folders if they were added
    run(["rm", "-r", "--cached", "mingit", "mingit_dist"])
    
    # 4. Add & Commit
    run(["add", "."])
    run(["commit", "-m", "Clean up and push code"])
    
    # 5. Push
    run(["push", "-u", "origin", "main", "--force"])

if __name__ == "__main__":
    clean_and_push()
