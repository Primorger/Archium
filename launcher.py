"""Archium Launcher - auto-update and launch the app"""

import subprocess
import sys
import json
import urllib.request
from pathlib import Path
import zipfile
import shutil
import tempfile
import os
import re
from datetime import datetime


class ArchiumLauncher:
    def __init__(self):
        if getattr(sys, "frozen", False):
            self.root_dir = Path(sys.executable).resolve().parent
        else:
            self.root_dir = Path(__file__).resolve().parent
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
    
    def check_for_updates(self):
        self.log("Checking for updates...")
        try:
            request = urllib.request.Request(
                self.github_api_url,
                headers={"User-Agent": "Archium-Updater"},
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "")
                if latest_version.lower().startswith("v"):
                    latest_version = latest_version[1:]
                
                download_url = None
                for asset in data.get('assets', []):
                    if asset.get('name', '').lower().endswith('.zip'):
                        download_url = asset.get('browser_download_url')
                        break
                
                if not self.compare_versions(latest_version, self.current_version):
                    self.log(f"Version {self.current_version} is current")
                    return
                if not download_url:
                    self.log(f"Release {latest_version} has no ZIP asset", "WARNING")
                    return
                
                self.log(f"Updating {self.current_version} → {latest_version}")
                if self.download_and_update(download_url, latest_version):
                    self.current_version = latest_version
        except Exception as e:
            self.log(f"Update check skipped ({type(e).__name__})")
    
    def compare_versions(self, latest, current):
        try:
            latest_parts = [int(part) for part in latest.split('.')]
            current_parts = [int(part) for part in current.split('.')]
            width = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (width - len(latest_parts)))
            current_parts.extend([0] * (width - len(current_parts)))
            return latest_parts > current_parts
        except (AttributeError, ValueError):
            return False
    
    def download_and_update(self, url, version):
        update_dir = Path(tempfile.mkdtemp(prefix=".archium-update-", dir=self.root_dir))
        archive_path = update_dir / "update.zip"
        extracted_dir = update_dir / "extracted"
        install_dir = update_dir / "install"
        backup_dir = update_dir / "backup"

        try:
            self.log("Downloading update...")
            urllib.request.urlretrieve(url, archive_path)

            self.log("Extracting update...")
            extracted_dir.mkdir()
            with zipfile.ZipFile(archive_path, 'r') as archive:
                root = extracted_dir.resolve()
                for member in archive.infolist():
                    destination = (extracted_dir / member.filename).resolve()
                    if os.path.commonpath((str(root), str(destination))) != str(root):
                        raise ValueError("Update archive contains an invalid path")
                archive.extractall(extracted_dir)

            payload_dir = extracted_dir
            if not (payload_dir / "archium.py").is_file():
                payload_dir = extracted_dir / ".archium"
            if not (payload_dir / "archium.py").is_file():
                raise ValueError("Update archive does not contain archium.py")

            payload_dir.rename(install_dir)

            for data_dir in ("db", "settings"):
                existing_data = self.app_dir / data_dir
                if existing_data.exists():
                    shutil.copytree(existing_data, install_dir / data_dir, dirs_exist_ok=True)

            version_path = install_dir / "version.json"
            with version_path.open('w', encoding='utf-8') as version_file:
                json.dump(
                    {'version': version, 'last_updated': datetime.now().isoformat()},
                    version_file,
                    indent=2,
                )

            if self.app_dir.exists():
                self.app_dir.rename(backup_dir)
            try:
                install_dir.rename(self.app_dir)
            except Exception:
                if backup_dir.exists():
                    backup_dir.rename(self.app_dir)
                raise

            self.log(f"Updated to {version}")
            return True
        except Exception as e:
            self.log(f"Update failed: {e}", "ERROR")
            if backup_dir.exists() and not self.app_dir.exists():
                backup_dir.rename(self.app_dir)
                self.log("Restored previous application")
            return False
        finally:
            shutil.rmtree(update_dir, ignore_errors=True)

    def find_python_command(self):
        candidates = []
        for executable in ("python", "python3"):
            path = shutil.which(executable)
            if path:
                candidates.append([path])

        py_launcher = shutil.which("py")
        if py_launcher:
            candidates.append([py_launcher, "-3"])

        for command in candidates:
            try:
                result = subprocess.run(
                    command + ["--version"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                )
            except (OSError, subprocess.SubprocessError):
                continue

            match = re.search(r"Python\s+(\d+)\.(\d+)", result.stdout + result.stderr)
            if result.returncode == 0 and match and tuple(map(int, match.groups())) >= (3, 8):
                return command
        return None

    def refresh_windows_path(self):
        if os.name != "nt":
            return

        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                machine_path = winreg.QueryValueEx(key, "Path")[0]
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                try:
                    user_path = winreg.QueryValueEx(key, "Path")[0]
                except FileNotFoundError:
                    user_path = ""
            os.environ["PATH"] = os.path.expandvars(f"{machine_path};{user_path}")
        except (ImportError, OSError):
            self.log("Could not refresh PATH; checking common Python locations")

    def install_python(self):
        if os.name != "nt":
            self.log("Automatic Python installation is supported on Windows only", "ERROR")
            return None

        self.log("Python 3.8+ was not found. Installing Python 3.11...")
        winget = shutil.which("winget")
        if winget:
            try:
                result = subprocess.run(
                    [
                        winget,
                        "install",
                        "--exact",
                        "--id",
                        "Python.Python.3.11",
                        "--scope",
                        "user",
                        "--silent",
                        "--accept-package-agreements",
                        "--accept-source-agreements",
                    ],
                    timeout=600,
                    check=False,
                )
                if result.returncode == 0:
                    self.refresh_windows_path()
                    command = self.find_python_command()
                    if command:
                        self.log("Python installed successfully")
                        return command
            except (OSError, subprocess.SubprocessError) as error:
                self.log(f"winget install failed ({type(error).__name__}); trying direct download")

        installer_dir = Path(tempfile.mkdtemp(prefix="archium-python-"))
        installer_path = installer_dir / "python-installer.exe"
        try:
            installer_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
            self.log("Downloading Python installer...")
            urllib.request.urlretrieve(installer_url, installer_path)

            self.log("Installing Python for the current user...")
            result = subprocess.run(
                [
                    str(installer_path),
                    "/quiet",
                    "InstallAllUsers=0",
                    "PrependPath=1",
                    "Include_test=0",
                    "Include_pip=1",
                ],
                timeout=600,
                check=False,
            )
            if result.returncode != 0:
                self.log("Python installer returned an error", "ERROR")
                return None

            self.refresh_windows_path()
            command = self.find_python_command()
            if command:
                self.log("Python installed successfully")
                return command
            self.log("Python installed, but no Python 3.8+ command was found", "ERROR")
            return None
        except (OSError, urllib.error.URLError, subprocess.SubprocessError) as error:
            self.log(f"Python installation failed: {error}", "ERROR")
            return None
        finally:
            shutil.rmtree(installer_dir, ignore_errors=True)

    def ensure_python(self):
        command = self.find_python_command()
        if command:
            self.log("Python 3.8+ found")
            return command
        return self.install_python()
    
    def launch(self):
        print("\n" + "="*50)
        print("         Archium")
        print("="*50 + "\n")
        
        self.check_for_updates()
        
        app_file = self.app_dir / "archium.py"
        if not app_file.exists():
            self.log(f"Error: {app_file} not found", "ERROR")
            return

        python_command = [sys.executable]
        if getattr(sys, "frozen", False):
            python_command = self.ensure_python()
            if not python_command:
                self.log("Install Python 3.8+ and run Archium.exe again.", "ERROR")
                return
        
        self.log("Launching...")
        subprocess.Popen(python_command + [str(app_file)], cwd=str(self.app_dir))


if __name__ == "__main__":
    try:
        ArchiumLauncher().launch()
    except Exception as e:
        print(f"\nError: {e}")
