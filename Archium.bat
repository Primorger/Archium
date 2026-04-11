@echo off
REM Archium Auto-Installer & Launcher
REM Installs Python if needed and runs Archium

setlocal enabledelayedexpansion
cd /d "%~dp0"

cls
echo.
echo ============================================================
echo         Archium - Auto-Installer
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python !PYTHON_VERSION! found
    echo.
    goto :launch
)

REM Python not found - try to install
echo [SETUP] Python not found
echo.

REM Try Windows Package Manager
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [SETUP] Installing Python via Windows Package Manager...
    winget install -e --id Python.Python.3.11 -h >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] Python installed
        echo.
        goto :launch
    )
)

REM Try direct download
echo [SETUP] Downloading Python 3.11...
if not exist "%temp%\archium_setup" mkdir "%temp%\archium_setup"

powershell -NoProfile -Command ^
    "$ProgressPreference='SilentlyContinue'; ^
    [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; ^
    try { ^
        Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' ^
        -OutFile '%temp%\archium_setup\python.exe' -UseBasicParsing; ^
        exit 0; ^
    } catch { ^
        exit 1; ^
    }" 2>nul

if !errorlevel! neq 0 (
    echo [ERROR] Failed to download Python
    echo Please install Python from https://www.python.org/downloads/
    echo Then run this batch file again
    pause
    exit /b 1
)

echo [SETUP] Installing Python (this may take a minute)...
"%temp%\archium_setup\python.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1 >nul 2>&1

if !errorlevel! neq 0 (
    echo [ERROR] Python installation failed
    pause
    exit /b 1
)

echo [OK] Python installed
rmdir /s /q "%temp%\archium_setup" 2>nul
timeout /t 2 /nobreak >nul 2>&1

:launch
echo ============================================================
echo         Starting Archium
echo ============================================================
echo.

python launcher.py

exit /b %errorlevel%

