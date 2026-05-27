import os
import sys
import zipfile
import urllib.request
import subprocess

workspace = r"c:\Users\AKGUL\Desktop\Abdüssamed\Gazi Ders\GaziMobilFinalEdizHoca"
git_dir = os.path.join(workspace, "temp_git")
zip_path = os.path.join(workspace, "mingit.zip")
url = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/MinGit-2.44.0-64-bit.zip"

def download_mingit():
    if os.path.exists(git_dir):
        print("temp_git already exists.")
        return True
    
    print(f"Downloading MinGit from {url}...")
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("Download completed.")
    except Exception as e:
        print(f"Error downloading: {e}")
        return False
    
    print("Extracting MinGit...")
    try:
        os.makedirs(git_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(git_dir)
        print("Extraction completed.")
        os.remove(zip_path)
        return True
    except Exception as e:
        print(f"Error extracting: {e}")
        return False

def run_git(args):
    git_bin = os.path.join(git_dir, "cmd", "git.exe")
    if not os.path.exists(git_bin):
        git_bin = os.path.join(git_dir, "bin", "git.exe")
    
    cmd = [git_bin] + args
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True)
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running git: {e}")
        return False

if __name__ == "__main__":
    if download_mingit():
        print("MinGit set up successfully.")
        
        # Test git version
        if run_git(["--version"]):
            # Configure credential helper to use windows manager so we can utilize existing cached GitHub credentials
            run_git(["config", "--global", "credential.helper", "manager"])
            
            # Run git status
            run_git(["status"])
            
            # Git add
            run_git(["add", "."])
            
            # Git commit
            # Let's check status first to see if there's anything to commit
            run_git(["commit", "-m", "feat: profile management, avatars upload, menus & announcements CRUD, pagination, and tests"])
            
            # Git push
            run_git(["push", "origin", "main"])
            
            print("Git commands execution complete.")
        else:
            print("Failed to run MinGit.")
    else:
        print("Failed to set up MinGit.")
