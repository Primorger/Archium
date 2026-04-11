# Archium Auto-Installer & Launcher
# Installs Python if needed and runs Archium

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
cd $PSScriptRoot

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         Archium - Auto-Installer" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCheck = & python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] $pythonCheck found" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[SETUP] Python not found" -ForegroundColor Yellow
    Write-Host "[SETUP] Downloading Python 3.11..." -ForegroundColor Yellow
    Write-Host ""
    
    # Create temp directory
    $tempDir = "$env:TEMP\archium_setup"
    New-Item -ItemType Directory -Path $tempDir -Force -ErrorAction SilentlyContinue | Out-Null
    
    # Download and install Python
    try {
        $url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
        $outPath = "$tempDir\python.exe"
        
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $progressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $url -OutFile $outPath -UseBasicParsing
        
        Write-Host "[OK] Download complete" -ForegroundColor Green
        Write-Host "[SETUP] Installing Python..." -ForegroundColor Yellow
        
        & $outPath /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python installed" -ForegroundColor Green
            Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            
            # Refresh PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        } else {
            throw "Installation failed"
        }
    } catch {
        Write-Host "[ERROR] Failed to install Python" -ForegroundColor Red
        Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         Starting Archium" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

& python launcher.py
