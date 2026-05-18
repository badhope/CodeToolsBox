@echo off
REM Global-Dev-Setup - One-Click Installer (Windows)

echo ============================================================
echo      Global-Dev-Setup - One-Click Installer
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.8+ from https://python.org
    echo.
    echo Press any key to open python.org...
    pause
    start https://python.org
    exit /b 1
)

echo Python found!
echo.

REM Select profile
echo Select your development profile:
echo.
echo 1) Full-Stack Web Developer
echo 2) AI/ML ^& Data Science
echo 3) DevOps ^& Cloud Native
echo 4) Mobile App Developer
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" set PROFILE=full-stack
if "%choice%"=="2" set PROFILE=ai-ml
if "%choice%"=="3" set PROFILE=devops
if "%choice%"=="4" set PROFILE=mobile
if "%PROFILE%"=="" set PROFILE=full-stack

echo.
echo Selected profile: %PROFILE%
echo.

REM Run the Python bootstrapper
echo Starting intelligent setup...
python bootstrap.py %PROFILE%

echo.
echo ============================================================
echo Setup complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Restart your terminal
echo   2. Check installed tools with: python global-dev-setup.py status
echo   3. For help: python global-dev-setup.py --help
echo.
pause
