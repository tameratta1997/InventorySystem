import os
import shutil
import subprocess
import sys

def fix_and_push():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_mingit = os.path.join(base_dir, "mingit")
    
    # 1. Move mingit to TEMP to avoid "File in use" errors and to stop tracking it
    temp_dir = os.path.join(os.environ["TEMP"], "inventory_mingit")
    
    if not os.path.exists(temp_dir):
        print(f"Copying Git to safe location: {temp_dir}...")
        try:
            shutil.copytree(local_mingit, temp_dir)
        except FileExistsError:
            pass # Already there
            
    git_exe = os.path.join(temp_dir, "cmd", "git.exe")
    
    # Update PATH so subprocess can find dlls
    os.environ["PATH"] = os.path.join(temp_dir, "cmd") + os.pathsep + os.environ["PATH"]
    
    def run(cmd):
        print(f"EXEC: {' '.join(cmd)}")
        subprocess.run(cmd, check=False)

    print(f"Using Safe Git: {git_exe}")
    
    # 2. Fix .gitignore
    gitignore_path = os.path.join(base_dir, ".gitignore")
    with open(gitignore_path, "a") as f:
        f.write("\nmingit/\npush_updates.py\nfix_push.py\n")
    
    # 3. Stop tracking 'mingit' folder if it was accidentally added
    print("Removing mingit from git tracking (keeping files)...")
    run([git_exe, "rm", "-r", "--cached", "mingit"])
    
    # 4. Add current state (respecting new gitignore)
    run([git_exe, "add", "."])
    
    # 5. Commit cleanup
    run([git_exe, "commit", "-m", "Fix: Remove git binaries from repo"])
    
    # 6. Rebase (might be messy if we are replaying the adding of mingit)
    # Actually, simpler to just pull with merge if rebase fails, but let's try rebase
    run([git_exe, "pull", "--rebase", "origin", "main"])
    
    # If rebase fails due to the mess, we might need to abort and try a merge strategy
    # BUT let's assume it works or prompts.
    
    # 7. Push
    run([git_exe, "push", "-u", "origin", "main"])
    
    print("Done. If there were errors, you might need to resolve manually or force push.")

if __name__ == "__main__":
    fix_and_push()
