@echo off
cd /d "%~dp0"
echo.
echo ========== Git Add ==========
git add .

echo.
echo ========== Git Commit ==========
set /p msg=Enter commit message: 
git commit -m "%msg%"

echo.
echo ========== Git Push ==========
git push origin main

pause
