# Build script to compile launcher.py to Archium.exe
# Run from root: .\scripts\build_exe.ps1
# Or from scripts folder: cd .. ; .\build_exe.ps1

Push-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Archium Launcher - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
$pyinstallerCheck = pip show pyinstaller 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

Write-Host ""
Write-Host "Building Archium.exe..." -ForegroundColor Green
Write-Host ""

# Build the exe
pyinstaller --onefile --console launcher.py --name=Archium --distpath=. --buildpath=build --specpath=.

Write-Host ""
if (Test-Path "Archium.exe") {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Build Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Archium.exe has been created in the root folder" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Verify GitHub repo in launcher.py:" -ForegroundColor Yellow
    Write-Host '   self.github_repo = "Primorger/Archium"' -ForegroundColor White
    Write-Host ""
    Write-Host "2. Update version.json to current version" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Create a GitHub Release with version tag" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "4. Attach app files as .zip to the release" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "5. Run Archium.exe to test" -ForegroundColor Yellow
    Write-Host ""
    Write-Host ""
} else {
    Write-Host "Build failed! Check the errors above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

# Clean up build artifacts
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }
Get-Item "*.spec" -ErrorAction SilentlyContinue | Remove-Item -ErrorAction SilentlyContinue

Pop-Location

Read-Host "Press Enter to exit"
