"""
Archium Launcher & Bootstrapper
Handles complete application setup and execution
"""

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
import time


class ArchiumBootstrapper:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.app_dir = self.root_dir / ".archium"
        self.venv_dir = self.root_dir / ".venv"
        self.version_file = self.app_dir / "version.json"
        self.github_repo = "Primorger/Archium"
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
        self.python_exe = self.venv_dir / "Scripts" / "python.exe" if sys.platform == "win32" else self.venv_dir / "bin" / "python"
        self.pip_exe = self.venv_dir / "Scripts" / "pip.exe" if sys.platform == "win32" else self.venv_dir / "bin" / "pip"
        self.current_version = self.load_current_version()
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60 + "\n")
    
    def print_status(self, text, status="INFO"):
        """Print status message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{status}] {text}")
    
    def load_current_version(self):
        """Load current version from version.json"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version', '0.0.0')
            except Exception as e:
                self.print_status(f"Failed to load version: {e}", "WARN")
                return '0.0.0'
        return '0.0.0'
    
    def save_version(self, version):
        """Save version to version.json"""
        try:
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'version': version,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.print_status(f"Failed to save version: {e}", "ERROR")
    
    def setup_venv(self):
        """Create virtual environment if it doesn't exist"""
        if self.venv_dir.exists():
            self.print_status("Virtual environment already exists", "SKIP")
            return True
        
        self.print_status("Creating virtual environment...", "SETUP")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_dir)],
                check=True,
                capture_output=True
            )
            self.print_status("Virtual environment created successfully", "OK")
            return True
        except Exception as e:
            self.print_status(f"Failed to create venv: {e}", "ERROR")
            return False
    
    def install_dependencies(self):
        """Install dependencies (mainly for future extensibility)"""
        self.print_status("Checking dependencies...", "SETUP")
        
        # For now, no external dependencies needed (Tkinter is built-in)
        # Upgrade pip first
        try:
            self.print_status("Upgrading pip...", "SETUP")
            subprocess.run(
                [str(self.pip_exe), "install", "--upgrade", "pip"],
                check=True,
                capture_output=True,
                timeout=60
            )
            self.print_status("Pip upgraded", "OK")
        except Exception as e:
            self.print_status(f"Warning: Could not upgrade pip: {e}", "WARN")
        
        # Note: Add requirements.txt parsing here if external dependencies are needed in future
        self.print_status("Dependencies ready (using Python standard library)", "OK")
        return True
    
    def check_for_updates(self):
        """Check GitHub for the latest version"""
        self.print_status("Checking for updates...", "UPDATE")
        
        try:
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
                    self.print_status("No release files found on GitHub", "WARN")
                    return False
                
                self.print_status(f"Current version: {self.current_version}", "INFO")
                self.print_status(f"Latest version: {latest_version}", "INFO")
                
                if self.compare_versions(latest_version, self.current_version):
                    self.print_status(f"New version available: {latest_version}", "UPDATE")
                    return self.download_and_update(download_url, latest_version)
                else:
                    self.print_status("Application is up to date", "OK")
                    return False
        
        except urllib.error.URLError:
            self.print_status("No internet connection - continuing with current version", "WARN")
            return False
        except Exception as e:
            self.print_status(f"Update check failed: {e}", "WARN")
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
            self.print_status(f"Downloading version {version}...", "UPDATE")
            
            zip_path = self.root_dir / "archium_update.zip"
            
            # Download the file
            urllib.request.urlretrieve(download_url, zip_path)
            self.print_status("Download complete", "OK")
            
            # Create backup of .archium directory
            backup_dir = self.root_dir / "backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            
            self.print_status("Backing up application files...", "UPDATE")
            
            if self.app_dir.exists():
                shutil.copytree(self.app_dir, backup_dir)
            
            # Extract the update to .archium
            self.print_status("Extracting update...", "UPDATE")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract all files to root first to check structure
                temp_extract = self.root_dir / "temp_extract"
                zip_ref.extractall(temp_extract)
                
                # Move app files to .archium
                if (temp_extract / ".archium").exists():
                    if self.app_dir.exists():
                        shutil.rmtree(self.app_dir)
                    shutil.move(str(temp_extract / ".archium"), str(self.app_dir))
                else:
                    # Fallback: assume files are in root of zip
                    if (temp_extract / "archium.py").exists():
                        if self.app_dir.exists():
                            shutil.rmtree(self.app_dir)
                        self.app_dir.mkdir(exist_ok=True)
                        for item in temp_extract.iterdir():
                            if item.name not in ['.git', '.venv', 'backup', 'scripts', 'Archium.exe', 'launcher.py']:
                                if item.is_dir():
                                    shutil.copytree(item, self.app_dir / item.name)
                                else:
                                    shutil.copy2(item, self.app_dir / item.name)
                
                shutil.rmtree(temp_extract)
            
            # Clean up
            zip_path.unlink()
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            
            self.current_version = version
            self.save_version(version)
            self.print_status(f"Successfully updated to version {version}", "OK")
            
            return True
        
        except Exception as e:
            self.print_status(f"Update failed: {e}", "ERROR")
            self.print_status("Restoring previous version...", "UPDATE")
            
            # Restore from backup if update failed
            backup_dir = self.root_dir / "backup"
            if backup_dir.exists():
                if self.app_dir.exists():
                    shutil.rmtree(self.app_dir)
                shutil.move(str(backup_dir), str(self.app_dir))
            
            self.print_status("Restored previous version", "OK")
            return False
    
    def run_archium(self):
        """Run the archium.py application"""
        try:
            archium_script = self.app_dir / "archium.py"
            
            if not archium_script.exists():
                self.print_status(f"Error: archium.py not found at {archium_script}", "ERROR")
                input("Press Enter to exit...")
                return False
            
            self.print_status(f"Launching Archium from {archium_script}...", "LAUNCH")
            
            # Run the script using the venv Python
            # Use Popen so parent process can exit
            subprocess.Popen([str(self.python_exe), str(archium_script)])
            
            self.print_status("Archium launched successfully", "OK")
            return True
        
        except Exception as e:
            self.print_status(f"Failed to launch Archium: {e}", "ERROR")
            input("Press Enter to exit...")
            return False
    
    def bootstrap(self):
        """Complete bootstrap process"""
        self.print_header("Archium Launcher & Bootstrapper v1.0")
        
        # Step 1: Setup virtual environment
        self.print_header("Step 1: Environment Setup")
        if not self.setup_venv():
            self.print_status("Could not set up virtual environment", "CRITICAL")
            time.sleep(3)
            return False
        
        # Step 2: Install dependencies
        self.print_header("Step 2: Dependencies")
        if not self.install_dependencies():
            self.print_status("Could not install dependencies", "CRITICAL")
            time.sleep(3)
            return False
        
        # Step 3: Check for updates
        self.print_header("Step 3: Update Check")
        self.check_for_updates()
        
        # Step 4: Launch application
        self.print_header("Step 4: Application Launch")
        return self.run_archium()


if __name__ == "__main__":
    try:
        bootstrapper = ArchiumBootstrapper()
        bootstrapper.bootstrap()
    except KeyboardInterrupt:
        print("\n\nShutdown requested by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

