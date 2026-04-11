import subprocess
import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
import zipfile
import shutil
from datetime import datetime


class ArchiumLauncher:
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.version_file = self.app_dir / "version.json"
        self.github_repo = "Primorger/Archium"  # Change this to your repo
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
        self.current_version = self.load_current_version()
    
    def load_current_version(self):
        """Load current version from version.json"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version', '0.0.0')
            except:
                return '0.0.0'
        return '0.0.0'
    
    def save_version(self, version):
        """Save version to version.json"""
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump({'version': version, 'last_updated': datetime.now().isoformat()}, f, indent=2)
    
    def check_for_updates(self):
        """Check GitHub for the latest version"""
        try:
            print("[Archium] Checking for updates...")
            
            with urllib.request.urlopen(self.github_api_url, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                latest_version = data.get('tag_name', '').lstrip('v')
                download_url = None
                
                # Find the zip file download URL
                for asset in data.get('assets', []):
                    if asset['name'].endswith('.zip'):
                        download_url = asset['browser_download_url']
                        break
                
                if not download_url:
                    print("[Archium] No release files found")
                    return False
                
                print(f"[Archium] Current version: {self.current_version}")
                print(f"[Archium] Latest version: {latest_version}")
                
                if self.compare_versions(latest_version, self.current_version):
                    return self.download_and_update(download_url, latest_version)
                else:
                    print("[Archium] Application is up to date")
                    return False
        
        except urllib.error.URLError:
            print("[Archium] Could not reach GitHub (no internet connection)")
            return False
        except Exception as e:
            print(f"[Archium] Update check failed: {str(e)}")
            return False
    
    def compare_versions(self, latest, current):
        """Compare semantic versions"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad with zeros if needed
            while len(latest_parts) < len(current_parts):
                latest_parts.append(0)
            while len(current_parts) < len(latest_parts):
                current_parts.append(0)
            
            return latest_parts > current_parts
        except:
            return False
    
    def download_and_update(self, download_url, version):
        """Download and extract the latest version"""
        try:
            print(f"[Archium] Downloading version {version}...")
            
            zip_path = self.app_dir / "archium_update.zip"
            
            # Download the file
            urllib.request.urlretrieve(download_url, zip_path)
            print("[Archium] Download complete")
            
            # Create backup
            backup_dir = self.app_dir / "backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            
            # Backup important files
            important_files = ['db', 'settings', 'version.json']
            backup_dir.mkdir(exist_ok=True)
            for item in important_files:
                item_path = self.app_dir / item
                if item_path.exists():
                    if item_path.is_dir():
                        shutil.copytree(item_path, backup_dir / item)
                    else:
                        shutil.copy2(item_path, backup_dir / item)
            
            print("[Archium] Extracting update...")
            
            # Extract the update
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.app_dir)
            
            # Restore backed up files
            for item in important_files:
                backup_item = backup_dir / item
                if backup_item.exists():
                    target_item = self.app_dir / item
                    if target_item.exists():
                        if target_item.is_dir():
                            shutil.rmtree(target_item)
                        else:
                            target_item.unlink()
                    
                    if backup_item.is_dir():
                        shutil.copytree(backup_item, target_item)
                    else:
                        shutil.copy2(backup_item, target_item)
            
            # Clean up
            zip_path.unlink()
            
            self.save_version(version)
            print(f"[Archium] Successfully updated to version {version}")
            
            return True
        
        except Exception as e:
            print(f"[Archium] Update failed: {str(e)}")
            print("[Archium] Restoring previous version...")
            
            # Restore from backup if update failed
            backup_dir = self.app_dir / "backup"
            if backup_dir.exists():
                for item in backup_dir.iterdir():
                    target_item = self.app_dir / item.name
                    if target_item.exists():
                        if target_item.is_dir():
                            shutil.rmtree(target_item)
                        else:
                            target_item.unlink()
                    
                    if item.is_dir():
                        shutil.copytree(item, target_item)
                    else:
                        shutil.copy2(item, target_item)
            
            return False
    
    def run_archium(self):
        """Run the archium.py application"""
        try:
            archium_script = self.app_dir / "archium.py"
            
            if not archium_script.exists():
                print("[Archium] Error: archium.py not found")
                input("Press Enter to exit...")
                return False
            
            print("[Archium] Launching Archium...")
            
            # Run the script with the same Python interpreter
            subprocess.Popen([sys.executable, str(archium_script)])
            return True
        
        except Exception as e:
            print(f"[Archium] Failed to launch Archium: {str(e)}")
            input("Press Enter to exit...")
            return False
    
    def launch(self):
        """Main launcher flow"""
        print("=" * 50)
        print("         Archium Launcher v1.0")
        print("=" * 50)
        
        # Check for updates
        self.check_for_updates()
        
        # Run Archium
        self.run_archium()


if __name__ == "__main__":
    launcher = ArchiumLauncher()
    launcher.launch()
