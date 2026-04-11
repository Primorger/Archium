"""Archium Launcher - auto-update and launch the app"""

import subprocess
import sys
import json
import urllib.request
from pathlib import Path
import zipfile
import shutil
from datetime import datetime


class ArchiumLauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.app_dir = self.root_dir / ".archium"
        self.version_file = self.app_dir / "version.json"
        self.github_repo = "Primorger/Archium"
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
        self.current_version = self.load_current_version()
    
    def log(self, msg, status="INFO"):
        print(f"[{status}] {msg}")
    
    def load_current_version(self):
        try:
            if self.version_file.exists():
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    return json.load(f).get('version', '0.0.0')
        except:
            pass
        return '0.0.0'
    
    def save_version(self, version):
        try:
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump({'version': version, 'last_updated': datetime.now().isoformat()}, f, indent=2)
        except:
            pass
    
    def check_for_updates(self):
        self.log("Checking for updates...")
        try:
            with urllib.request.urlopen(self.github_api_url, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get('tag_name', '').lstrip('v')
                
                download_url = None
                for asset in data.get('assets', []):
                    if asset['name'].endswith('.zip'):
                        download_url = asset['browser_download_url']
                        break
                
                if not download_url or not self.compare_versions(latest_version, self.current_version):
                    self.log(f"Version {self.current_version} is current")
                    return
                
                self.log(f"Updating {self.current_version} → {latest_version}")
                self.download_and_update(download_url, latest_version)
        except Exception as e:
            self.log(f"Update check skipped ({type(e).__name__})")
    
    def compare_versions(self, latest, current):
        try:
            l = [int(x) for x in latest.split('.')]
            c = [int(x) for x in current.split('.')]
            while len(l) < len(c):
                l.append(0)
            while len(c) < len(l):
                c.append(0)
            return l > c
        except:
            return False
    
    def download_and_update(self, url, version):
        try:
            zip_path = self.root_dir / "archium_update.zip"
            backup_dir = self.root_dir / "backup"
            
            # Backup
            if self.app_dir.exists() and backup_dir.exists():
                shutil.rmtree(backup_dir)
            if self.app_dir.exists():
                shutil.copytree(self.app_dir, backup_dir)
            
            # Download and extract
            self.log("Downloading...")
            urllib.request.urlretrieve(url, zip_path)
            
            self.log("Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(self.root_dir)
            
            zip_path.unlink()
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            
            self.save_version(version)
            self.log(f"Updated to {version}")
        except Exception as e:
            self.log(f"Update failed: {e}", "ERROR")
            # Restore backup
            backup_dir = self.root_dir / "backup"
            if backup_dir.exists():
                if self.app_dir.exists():
                    shutil.rmtree(self.app_dir)
                shutil.move(str(backup_dir), str(self.app_dir))
                self.log("Restored backup")
    
    def launch(self):
        print("\n" + "="*50)
        print("         Archium")
        print("="*50 + "\n")
        
        self.check_for_updates()
        
        app_file = self.app_dir / "archium.py"
        if not app_file.exists():
            self.log(f"Error: {app_file} not found", "ERROR")
            return
        
        self.log("Launching...")
        subprocess.Popen([sys.executable, str(app_file)])


if __name__ == "__main__":
    try:
        ArchiumLauncher().launch()
    except Exception as e:
        print(f"\nError: {e}")
