@echo off
REM Setup script dla Selenium Tests na Windows

echo.
echo ======================================
echo Selenium Tests - PrestaShop Setup
echo ======================================
echo.

REM Sprawdź Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python nie znaleziony! Zainstaluj Python 3.7+
    exit /b 1
)

echo [OK] Python znaleziony

REM Zainstaluj requirements
echo.
echo Instalowanie zaleznoci...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Nie udalo sie zainstalowac zaleznosci
    exit /b 1
)

echo.
echo ======================================
echo Setup zakonczony!
echo ======================================
echo.
echo Aby uruchomic testy, wykonaj:
echo   python run_tests.py
echo.
echo Lub bezposrednio z pytest:
echo   cd selenium
echo   pytest -v -s
echo.
