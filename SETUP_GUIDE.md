# Archium - Complete Setup Guide

## 📦 What is Archium?

Archium is a library management helper application that requires **ZERO manual setup**. Clone the repo, run the exe, and everything works automatically.

## 🚀 For Users (Running the Application)

### The One-Step Process

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Primorger/Archium.git
   cd Archium
   ```

2. **Run Archium.exe**:
   ```bash
   Archium.exe
   ```

That's it. The application will automatically:
- ✅ Create a Python virtual environment (`.venv` folder)
- ✅ Install all dependencies (uses standard library only)
- ✅ Check GitHub for new versions
- ✅ Download and install updates (if available)
- ✅ Launch the application
- ✅ Preserve your data (db/ and settings/) across updates

### What You'll See

```
============================================================
  Archium Launcher & Bootstrapper v1.0
============================================================

[14:32:01] [SETUP] Creating virtual environment...
[14:32:15] [OK] Virtual environment created successfully
[14:32:15] [SETUP] Checking dependencies...
[14:32:16] [OK] Dependencies ready (using Python standard library)
[14:32:16] [UPDATE] Checking for updates...
[14:32:18] [OK] Application is up to date
[14:32:18] [LAUNCH] Launching Archium...
[14:32:18] [OK] Archium launched successfully
```

After which the GUI opens automatically.

### What Gets Hidden

All internal workings are in the `.archium` folder (hidden on Windows):
```
.archium/
├── archium.py          # Main GUI application
├── version.json        # Version info
├── classes_and_funcs/  # Core modules
├── db/                 # Your library database
└── settings/           # Your preferences
```

The user only sees:
- `Archium.exe` - **Just run this**
- `.archium/` - Hidden system folder (ignore)
- `.venv/` - Hidden Python environment (auto-managed)
- `.git/` - Hidden git repo (for developers)

## 🔧 For Developers (Building & Deploying)

### Repository Structure

```
Archium/
├── 📄 Archium.exe              # User-facing executable
├── 📄 launcher.py              # Bootstrapper (compiles to exe)
│
├── 📁 .archium/                # Hidden app wrapper
│   ├── archium.py              # Main application
│   ├── version.json            # Current version
│   ├── classes_and_funcs/
│   ├── db/
│   └── settings/
│
├── 📁 scripts/                 # Build tools
│   ├── build_exe.bat
│   └── build_exe.ps1
│
├── 📁 .github/workflows/        # CI/CD automation
│   └── build.yml
│
├── 📁 .venv/                   # User's Python environment (auto-created)
└── 📋 Documentation files
```

### Making Changes

1. **Edit source files** in `.archium/`:
   ```bash
   # Edit the main application
   code .archium/archium.py
   
   # Edit core modules
   code .archium/classes_and_funcs/
   ```

2. **Test locally**:
   ```bash
   python .archium/archium.py
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

### Publishing a New Version

#### Step 1: Update Version
Edit `.archium/version.json`:
```json
{
  "version": "2.0.1",
  "last_updated": "2026-04-11T14:00:00"
}
```

#### Step 2: Rebuild Executable (Optional - CI/CD does this)
```bash
cd scripts
./build_exe.ps1    # Creates Archium.exe
```

#### Step 3: Create GitHub Release
1. Go to GitHub repo → Releases → Create New Release
2. Tag: `v2.0.1` (matches `.archium/version.json`)
3. Title: `Archium 2.0.1`
4. Add release notes
5. Attach `.zip` file with:
   ```
   archium-2.0.1.zip
   ├── .archium/
   ├── launcher.py
   ├── scripts/
   └── (other files except .venv, .git, build/)
   ```

#### Step 4: Automatic Upload (GitHub Actions)
- GitHub Actions automatically builds `Archium.exe`
- Exe is uploaded to the release
- Users get auto-update when they run the app

### Local Build Process

If you need to rebuild the exe:

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Navigate to scripts folder
cd scripts

# 3. Run build script
./build_exe.ps1      # PowerShell
# or
build_exe.bat        # Command Prompt

# 4. Archium.exe is created in root folder
```

## 🔄 Update Flow (Automatic)

When user runs `Archium.exe`:

```
1. Launcher reads .archium/version.json (e.g., "2.0.0")
   ↓
2. Checks GitHub API for latest release tag
   ↓
3. Compares versions using semantic versioning
   ↓
4. If newer version available:
   - Creates backup of .archium/
   - Downloads release .zip
   - Extracts to .archium/
   - Restores backup if errors
   ↓
5. Creates .venv/ if doesn't exist
   ↓
6. Installs/upgrades pip in venv
   ↓
7. Launches archium.py inside venv
```

**User data preserved**: `db/` and `settings/` folders are backed up before updates.

## ⚙️ Configuration

### GitHub Repository
Edit `launcher.py` line 21 (if needed):
```python
self.github_repo = "Primorger/Archium"  # Your repo here
```

### Version Sync
Keep these in sync:
- **GitHub Release tag**: `v2.0.1`
- **`.archium/version.json`**: `"version": "2.0.1"`

Mismatch will prevent auto-updates from working correctly.

## 📋 Dependency Management

Currently using **only Python standard library** (Tkinter, json, subprocess, urllib, zipfile, etc.)

To add future dependencies:
1. Update `requirements.txt`:
   ```
   requests==2.28.0
   ```
2. Modify `launcher.py` `install_dependencies()` to read requirements.txt
3. Dependencies auto-install in user's venv on first run

## 🐛 Troubleshooting

### "Virtual environment failed to create"
- **Cause**: Python not in PATH or 32-bit Python
- **Fix**: Ensure Python 3.6+ is installed (64-bit) and in system PATH

### "Archium.py not found"
- **Cause**: `.archium/` folder missing or corrupted
- **Fix**: Re-clone repo: `git clone https://github.com/Primorger/Archium.git`

### "Update failed"
- **Cause**: Internet disconnected or GitHub unreachable
- **Fix**: Application continues with current version; try again later

### "Application won't launch"
- **Cause**: Tkinter not installed with Python
- **Fix**: Reinstall Python with Tkinter option enabled

## 🔐 Security Notes

- Exe is built from open-source launcher.py (audit-able)
- All dependencies are from Python standard library (no external risks)
- Updates pulled from official GitHub releases (HTTPS)
- User data never sent to external servers

## 📊 File Locations

| Item | Location | Hidden? | Auto-created? |
|------|----------|---------|---------------|
| Application | `.archium/` | Yes | No (in repo) |
| Python env | `.venv/` | Yes | Yes (first run) |
| User data (db) | `.archium/db/` | Yes | Yes (first save) |
| User settings | `.archium/settings/` | Yes | Yes (first change) |
| Version info | `.archium/version.json` | Yes | No (in repo) |

## 🎯 Release Checklist

Before creating GitHub Release:

- [ ] Updated `.archium/version.json` version number
- [ ] Tested locally: `python .archium/archium.py`
- [ ] All changes committed and pushed
- [ ] Created `.zip` file with `.archium/` and other files
- [ ] Created GitHub Release with correct tag
- [ ] Attached `.zip` to release
- [ ] Verified GitHub Actions builds exe successfully

## 📚 Additional Resources

- [README.md](README.md) - User documentation
- [QUICKSTART.md](QUICKSTART.md) - Developer quick reference
- [REPO_STRUCTURE.md](REPO_STRUCTURE.md) - Detailed file structure

## 💬 Support

For issues:
1. Check [GitHub Issues](https://github.com/Primorger/Archium/issues)
2. Review logs in console output
3. Ensure Python 3.6+ is installed
4. Check internet connection for update checks

---

**Zero-setup philosophy**: From `git clone` to running app in under 10 seconds. Everything else is automatic.
