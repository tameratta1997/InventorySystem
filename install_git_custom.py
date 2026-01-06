import urllib.request
import zipfile
import os

def install_mingit():
    url = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/MinGit-2.43.0-64-bit.zip"
    dest_zip = "mingit.zip"
    dest_dir = "mingit"
    
    if not os.path.exists(dest_dir):
        print("Downloading MinGit...")
        urllib.request.urlretrieve(url, dest_zip)
        
        print("Extracting...")
        with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
            
        print("Done.")
    else:
        print("MinGit already exists.")
        
    return os.path.abspath(os.path.join(dest_dir, "cmd", "git.exe"))

if __name__ == "__main__":
    git_path = install_mingit()
    print(f"Git Path: {git_path}")
