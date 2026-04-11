# Repository Structure Guide

## 📁 Project Layout

```
Archium/
│
├── 📄 archium.py              # Main application entry point
├── 📄 launcher.py             # Update launcher (checks GitHub for new versions)
├── 📄 version.json            # Current version (synced with GitHub releases)
├── 📄 README.md               # Full documentation
├── 📄 QUICKSTART.md          # Quick start guide for developers
├── 📋 requirements.txt        # Python dependencies (mostly standard library)
├── 📋 .gitignore             # Git ignore patterns
│
├── 📁 classes_and_funcs/      # Core application modules
│   ├── 📄 book.py            # Book data class
│   └── 📄 library.py         # Library management class
│
├── 📁 db/                     # Book database files
│   ├── 📄 lib.txt            # Library files (pipe-delimited: title|author|genre|year|length|country|place)
│   └── 📄 *.txt              # One file per library
│
├── 📁 settings/               # User settings storage
│   └── 📄 settings.json       # Saved user preferences (language, font sizes)
│
├── 📁 scripts/                # Build and utility scripts
│   ├── 📄 build_exe.bat       # Build exe (Windows CMD)
│   ├── 📄 build_exe.ps1       # Build exe (PowerShell)
│   └── 📄 LAUNCHER_SETUP.md   # Build documentation
│
├── 📁 .github/               # GitHub-specific files
│   └── 📁 workflows/         # GitHub Actions CI/CD
│       └── 📄 build.yml      # Auto-build on release (creates exe + zip)
│
├── 📄 Archium.exe            # Compiled executable (auto-generated)
└── 📁 .git/                  # Git repository
```

## 🚀 Quick Commands

### Run Application
```bash
python archium.py
```

### Run with Auto-Updates
```bash
python launcher.py
```

### Build Executable
```bash
cd scripts
build_exe.bat              # Windows CMD
# or
./build_exe.ps1            # PowerShell
```

### Publish New Version
1. Update `version.json` with new version
2. Create GitHub Release with tag `v{version}`
3. Attach `archium-{version}.zip` to release
4. GitHub Actions automatically builds exe + archives

## 📊 File Purposes

| File | Purpose |
|------|---------|
| `archium.py` | Main GUI application using Tkinter |
| `launcher.py` | Auto-updater that checks GitHub releases |
| `version.json` | Tracks current version, used by launcher |
| `classes_and_funcs/book.py` | Book class (attributes + methods) |
| `classes_and_funcs/library.py` | Library class (search, CRUD operations) |
| `db/*.txt` | Persistent book storage (pipe-delimited) |
| `settings/settings.json` | User preferences (language, UI font size) |
| `Archium.exe` | Compiled launcher (distribution executable) |
| `.github/workflows/build.yml` | CI/CD automation for releases |

## 🔄 Workflow

### Development Flow
1. Make changes to code
2. Test: `python archium.py`
3. Commit: `git add . && git commit -m "message"`
4. Push: `git push origin main`

### Release Flow
1. Update `version.json` version number
2. Commit and push
3. Create GitHub Release:
   - Tag: `v2.0.1` (matches version.json)
   - Attach release archive zip
4. GitHub Actions automatically:
   - Builds `Archium.exe`
   - Creates release zip archive
   - Uploads both to GitHub Release
5. Users auto-receive update when running `Archium.exe`

## 📝 Key Configuration

### GitHub Repository
Set in `launcher.py` line 18:
```python
self.github_repo = "Primorger/Archium"
```

### Version Sync
`version.json` must match GitHub release tag (without 'v' prefix):
- GitHub tag: `v2.0.1`
- `version.json`: `"version": "2.0.1"`

### Auto-Update
The launcher:
1. Reads current version from `version.json`
2. Checks GitHub API for latest release
3. Compares versions (semantic versioning)
4. Downloads `.zip` if newer available
5. Backs up user data (db/, settings/)
6. Extracts update
7. Restores user data
8. Runs `archium.py`

## 🛠️ Building & Deployment

### Local Build
```bash
cd scripts
./build_exe.ps1  # Creates Archium.exe in root
```

### CI/CD Build (GitHub Actions)
- Automatic on every release tag push
- `.github/workflows/build.yml` handles:
  - Python environment setup
  - PyInstaller compilation
  - Release archive creation
  - Upload to GitHub Release

### Distribution
- Users download `Archium.exe`
- Exe contains launcher + auto-updater
- First run checks for updates
- Subsequent runs auto-update if available

## 📦 Release Checklist

Before creating a GitHub Release:
- [ ] Update `version.json` version number
- [ ] Test locally: `python archium.py`
- [ ] Build exe: `cd scripts && ./build_exe.ps1`
- [ ] Create release archive zip with all app files
- [ ] Commit changes and push
- [ ] Create GitHub Release with:
  - [ ] Tag: `v{version}` (matches version.json)
  - [ ] Release notes describing changes
  - [ ] Attached `.zip` file with all app files
  - [ ] Exe will be auto-built by GitHub Actions

## 🔗 Important Links

- GitHub Repo: https://github.com/Primorger/Archium
- Releases: https://github.com/Primorger/Archium/releases
- Issues: https://github.com/Primorger/Archium/issues
- Wiki: https://github.com/Primorger/Archium/wiki (optional)

## 💡 Development Tips

1. **Testing search**: Use Bulgarian characters (Cyrillic) to test Unicode support
2. **Testing updates**: Create a draft release to see if updater finds it
3. **Backup strategy**: User data (db/, settings/) preserved during updates
4. **Version format**: Always use semantic versioning (MAJOR.MINOR.PATCH)
5. **GitHub setup**: Ensure repo is public so launcher can access releases
