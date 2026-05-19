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
echo ============================================================
echo              Select your development profile
echo ============================================================
echo.
echo === Web Development ===
echo  1) Full-Stack Web Developer
echo  2) Frontend Developer
echo  3) Backend Developer
echo.
echo === AI ^& Machine Learning ===
echo  4) AI/ML Developer
echo  5) AI Agent Developer
echo  6) ML Engineer
echo  7) Data Scientist
echo.
echo === Big Data ^& Data Engineering ===
echo  8) Big Data Engineer
echo  9) Data Engineer
echo.
echo === DevOps ^& Cloud ===
echo 10) DevOps Engineer
echo 11) Cloud Native Developer
echo 12) System Administrator
echo.
echo === Mobile ^& Game ===
echo 13) Mobile App Developer
echo 14) Game Developer
echo.
echo === Specialized ===
echo 15) Blockchain Developer
echo 16) IoT Developer
echo 17) Embedded Developer
echo 18) Security Engineer
echo 19) QA/Testing Engineer
echo.
echo === Language-Specific ===
echo 20) Python Developer
echo 21) Java Developer
echo 22) Go Developer
echo 23) Rust Developer
echo.
set /p choice="Enter your choice (1-23): "

if "%choice%"=="1" set PROFILE=full-stack
if "%choice%"=="2" set PROFILE=frontend
if "%choice%"=="3" set PROFILE=backend
if "%choice%"=="4" set PROFILE=ai-ml
if "%choice%"=="5" set PROFILE=ai-agent
if "%choice%"=="6" set PROFILE=ml-engineer
if "%choice%"=="7" set PROFILE=data-science
if "%choice%"=="8" set PROFILE=big-data
if "%choice%"=="9" set PROFILE=data-engineering
if "%choice%"=="10" set PROFILE=devops
if "%choice%"=="11" set PROFILE=cloud-native
if "%choice%"=="12" set PROFILE=sysadmin
if "%choice%"=="13" set PROFILE=mobile
if "%choice%"=="14" set PROFILE=game-dev
if "%choice%"=="15" set PROFILE=blockchain
if "%choice%"=="16" set PROFILE=iot
if "%choice%"=="17" set PROFILE=embedded
if "%choice%"=="18" set PROFILE=security
if "%choice%"=="19" set PROFILE=qa
if "%choice%"=="20" set PROFILE=python
if "%choice%"=="21" set PROFILE=java
if "%choice%"=="22" set PROFILE=go
if "%choice%"=="23" set PROFILE=rust
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
