# Archium Deployment & Release Guide

## 🎯 Vision: Zero Setup for Users

Users should only need to:
1. Clone repo: `git clone https://github.com/Primorger/Archium.git`
2. Run exe: `Archium.exe`
3. That's it - everything else is automatic

## 👥 For End Users

### Installation

```bash
git clone https://github.com/Primorger/Archium.git
cd Archium
Archium.exe
```

**What happens automatically:**
- ✅ Creates hidden `.venv/` Python environment
- ✅ Installs dependencies (using standard library)
- ✅ Checks GitHub for newer versions
- ✅ Downloads and installs updates (if available)
- ✅ Preserves user data (db/ and settings/) across updates
- ✅ Launches the GUI

**The user never sees or needs to do anything else.**

### Data Location

User data is stored in `.archium/` (hidden folder):
- **Books**: `.archium/db/` (one `.txt` file per library)
- **Settings**: `.archium/settings/settings.json`
- **Version**: `.archium/version.json`

The user doesn't need to know this exists.

## 👨‍💻 For Developers

### Repository Structure

```
Archium/
├── Archium.exe                 # Compiled launcher (built from launcher.py)
├── launcher.py                 # Bootstrap code (what gets compiled to exe)
│
├── .archium/                   # Application wrapper (hidden on Windows)
│   ├── archium.py              # Main GUI code
│   ├── version.json            # Current version (e.g., "2.0.0")
│   ├── classes_and_funcs/      # Core modules
│   │   ├── book.py
│   │   └── library.py
│   ├── db/                     # User book data
│   └── settings/               # User preferences
│
├── scripts/                    # Build tools
│   ├── build_exe.bat
│   └── build_exe.ps1
│
├── .github/workflows/          # CI/CD automation
│   └── build.yml               # Auto-builds exe on release
│
├── .venv/                      # Created on first user run (not in git)
│
└── docs/                       # Documentation
    ├── README.md
    ├── SETUP_GUIDE.md
    ├── QUICKSTART.md
    ├── REPO_STRUCTURE.md
    └── DEPLOYMENT.md (this file)
```

### Making Code Changes

Edit files in `.archium/`:

```bash
# Edit the main application
code .archium/archium.py

# Edit core modules
code .archium/classes_and_funcs/

# Test your changes
python .archium/archium.py

# Commit and push
git add .
git commit -m "Describe your changes"
git push origin main
```

### Version Numbering

Use [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `2.0.1`)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

## 📦 Release Process

### Step 1: Prepare Release

**1.1 Update version in `.archium/version.json`:**
```json
{
  "version": "2.0.1",
  "last_updated": "2026-04-11T14:00:00"
}
```

**1.2 Commit changes:**
```bash
git add .archium/version.json
git commit -m "Release version 2.0.1"
git push origin main
```

### Step 2: Create Release Archive

Create a `.zip` file containing:
```
archium-2.0.1.zip
├── .archium/
│   ├── archium.py
│   ├── version.json          (must be "2.0.1")
│   ├── classes_and_funcs/
│   ├── db/                   (with sample libraries)
│   └── settings/
├── launcher.py
├── scripts/                  (optional)
└── README.md                 (optional)
```

**Do NOT include:**
- `.venv/` - User creates this
- `.git/` - Git handles this
- `build/` or `dist/` - Build artifacts
- `.pyc` or `__pycache__/` - Python cache
- `Archium.exe` - We'll rebuild this

### Step 3: Create GitHub Release

1. Go to: https://github.com/Primorger/Archium/releases
2. Click: "Create a new release"
3. Fill in:
   - **Tag**: `v2.0.1` (MUST match version.json minus the 'v')
   - **Title**: `Archium 2.0.1`
   - **Description**: Release notes (what changed, bugs fixed, etc.)
4. Upload created `.zip` file
5. Click: "Publish release"

### Step 4: GitHub Actions Auto-builds

When you publish the release:
1. GitHub Actions workflow triggers (`.github/workflows/build.yml`)
2. Automatically:
   - Builds `Archium.exe` from `launcher.py`
   - Creates release archive `.zip`
   - Uploads both to the release
3. **No manual build needed!**

### Step 5: Users Get Updates

When existing users run `Archium.exe`:
1. Launcher checks GitHub API
2. Compares version: current (2.0.0) vs latest (2.0.1)
3. If newer found:
   - Downloads `.zip` from release
   - Backs up `.archium/` folder
   - Extracts new files
   - Restores backup if errors
   - Saves new version
4. Launches application with new code

**Users don't need to do anything - it's automatic!**

## 🔄 Update Mechanism Flow

```
User runs Archium.exe
    ↓
Launcher reads .archium/version.json (e.g., "2.0.0")
    ↓
Queries GitHub API: /repos/Primorger/Archium/releases/latest
    ↓
Compares versions (is v2.0.1 > 2.0.0? YES)
    ↓
Downloads archium-2.0.1.zip (from release assets)
    ↓
Backs up .archium/ to backup/
    ↓
Extracts zip to .archium/
    ↓
If any error: restore .archium/ from backup/
    ↓
Updates .archium/version.json to "2.0.1"
    ↓
Deletes backup/ and zip
    ↓
Creates .venv/ if doesn't exist
    ↓
Upgrades pip in .venv/
    ↓
Runs .archium/archium.py inside .venv/
    ↓
GUI launches
```

## ⚙️ Configuration

### GitHub Repository URL

In `launcher.py` (line 21), verify:
```python
self.github_repo = "Primorger/Archium"
```

### CI/CD Workflow

GitHub Actions (`.github/workflows/build.yml`) is configured to:
1. Trigger on every release tag push
2. Set up Python 3.11
3. Install PyInstaller
4. Build `Archium.exe`
5. Create release archive
6. Upload to release

No changes needed unless you change repo name.

## 🐛 Troubleshooting Deployment

### "Users not getting updates"

**Issue**: Version in GitHub doesn't match `.archium/version.json`

**Fix**: Ensure exact match:
- GitHub tag: `v2.0.1`
- `.archium/version.json`: `"2.0.1"`
- Launcher compares after stripping 'v'

### "Exe isn't auto-built by GitHub Actions"

**Issue**: Workflow not triggered or failed

**Fix**: Check workflow runs at: https://github.com/Primorger/Archium/actions

Look for successful build with release tag.

### "Users report 'No release files found'"

**Issue**: Release created but no `.zip` attached

**Fix**: Ensure `.zip` file is uploaded as release asset (not release body)

### "Update fails for users"

**Common causes:**
1. Internet disconnected - Launcher retries, continues with old version
2. `.zip` corrupt - Backup automatically restored
3. GitHub unreachable - Application continues with current version

All failures gracefully degrade.

## 📊 Release Checklist

Before creating GitHub Release:

**Code Readiness**
- [ ] All changes tested locally: `python .archium/archium.py`
- [ ] No debug code or print statements left in production
- [ ] Code follows Python style guidelines
- [ ] All features documented in code comments

**Documentation**
- [ ] Updated `.archium/version.json` version
- [ ] Wrote release notes describing changes
- [ ] Updated README if user-facing changes
- [ ] Added migration notes if data format changed

**Testing**
- [ ] Tested locally with Python 3.6+
- [ ] Tested search with Unicode characters
- [ ] Tested all dialogs and buttons
- [ ] Tested settings save/load
- [ ] Tested on clean install scenario

**Release Archive**
- [ ] Created `.zip` with all required files
- [ ] Verified `.archium/version.json` in zip matches release tag
- [ ] No `__pycache__`, `.pyc`, `.venv`, or `.git` in zip
- [ ] Tested extracting zip doesn't overwrite user data

**GitHub Release**
- [ ] Created release with tag `v{version}`
- [ ] Added descriptive release notes
- [ ] Uploaded `.zip` as asset
- [ ] Verified GitHub Actions builds exe automatically
- [ ] Downloaded and tested auto-built exe locally

## 📚 Documentation Files

- **README.md** - User-facing overview and quick start
- **SETUP_GUIDE.md** - Complete setup for users and developers
- **QUICKSTART.md** - Developer quick reference
- **REPO_STRUCTURE.md** - Detailed file organization
- **DEPLOYMENT.md** - This file (release and deployment guide)

## 🔐 Security Considerations

1. **Exe Source**: Built from open repository - users can audit code
2. **Dependencies**: Only Python standard library (no external packages = no supply chain attacks)
3. **Updates**: Downloaded over HTTPS from official GitHub
4. **User Data**: Never leaves user's machine (no phoning home)
5. **Backup**: User data backed up before every update

## 🎓 Learning Resources

### For new developers:
- Start with [README.md](README.md)
- Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for architecture
- Reference [QUICKSTART.md](QUICKSTART.md) for common tasks

### For release management:
- This file covers the complete process
- Bookmark GitHub repo: https://github.com/Primorger/Archium
- Watch Actions tab for build status

### For troubleshooting:
- Check GitHub Issues: https://github.com/Primorger/Archium/issues
- Review console output when running locally
- Check `.venv/` creation and pip upgrade logs

## 🚀 Next Release Quick Reference

```bash
# 1. Make changes
# 2. Test:
python .archium/archium.py

# 3. Update version
# Edit .archium/version.json

# 4. Commit
git add .
git commit -m "Release 2.0.1"
git push origin main

# 5. Create .zip
# (Include .archium/, launcher.py, scripts/)

# 6. Create GitHub Release
# - Tag: v2.0.1
# - Upload .zip
# - Publish

# That's it! GitHub Actions builds exe automatically.
# Users get auto-update when they next run Archium.exe
```

---

**Philosophy**: Zero friction for users. Automatic everything. One-click releases.
