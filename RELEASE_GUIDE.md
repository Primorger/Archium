# Archium Release Guide

This guide explains how to publish a new release of Archium.

## Quick Summary

Release process is **automatic** through GitHub Actions:

1. Update version in `.archium/version.json`
2. Commit and push to GitHub
3. Create a GitHub Release with the version tag
4. GitHub Actions automatically builds the `.exe` file
5. Done!

## Step-by-Step Release Instructions

### 1. Update the Version

Edit `.archium/version.json` and increment the version following semantic versioning (MAJOR.MINOR.PATCH):

```json
{
    "version": "2.0.1"
}
```

Examples:
- **2.0.0** → **2.0.1** = patch (bug fixes)
- **2.0.0** → **2.1.0** = minor (new features)
- **2.0.0** → **3.0.0** = major (breaking changes)

### 2. Commit and Push

```bash
git add .archium/version.json
git commit -m "Release v2.0.1"
git push
```

### 3. Create GitHub Release

Go to your GitHub repository:

1. Click **Releases** (on the right sidebar)
2. Click **Create a new release**
3. **Tag version**: Enter `v2.0.1` (must match version.json with `v` prefix)
4. **Release title**: `Archium 2.0.1`
5. **Description**: Write what changed (e.g., "Bug fixes and performance improvements")
6. Click **Publish release**

GitHub Actions will automatically:
- Build the `.exe` using PyInstaller
- Attach the compiled Archium.exe to the release
- You can see progress in the **Actions** tab

### 4. Verify Release

Once GitHub Actions completes:
- Check the **Releases** page
- Confirm that `Archium.exe` is attached to the release
- Test downloading and running it to ensure it works

## Files Changed During Release

Only change:
- `.archium/version.json` (update version number)

Do NOT change:
- launcher.py
- Archium.bat
- Archium.ps1
- Any source code (unless adding features or fixing bugs)

## Distribution

Users download the latest release from:
- **GitHub Releases page** (recommended): https://github.com/your-username/Archium/releases
- Or clone the repository: `git clone https://github.com/your-username/Archium.git`

## Troubleshooting

**GitHub Actions failed to build**
- Check the **Actions** tab for error logs
- Verify `launcher.py` is syntactically correct
- Ensure `.archium/version.json` is valid JSON

**Release tag not found**
- Tag format must include `v` prefix: `v2.0.1`
- Tag must exactly match version.json version (with `v` in tag only)

**Users can't download .exe**
- Check GitHub Release is published (not a draft)
- Verify Archium.exe file is attached to the release

## Checklist Before Release

- [ ] All features tested and working
- [ ] Bugs fixed
- [ ] `.archium/version.json` updated
- [ ] Commit message clear and descriptive
- [ ] GitHub Release created with correct tag format
- [ ] Release description explains what changed
- [ ] Downloaded .exe tested on a clean Windows system

## After Release

1. Announce on any relevant channels (Discord, social media, etc.)
2. Users will be notified of the update when they run Archium (automatic checking)
3. Old users can manually check for updates or wait for auto-refresh
4. Keep GitHub updated with release notes

---

**Note**: The launcher automatically checks GitHub for updates when users run Archium, so users don't need to manually download new versions. They can click the update notification when available.
