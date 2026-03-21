@echo off
echo.
echo ========================================
echo    WeatherWise - Auto Setup Script
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/6] Installing packages...
pip install -r requirements.txt

echo.
echo [3/6] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created!
    echo Please edit .env file with your settings before continuing.
    pause
) else (
    echo .env file already exists!
)

echo.
echo [4/6] Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo [5/6] Creating superuser...
echo Please create your admin account:
python manage.py createsuperuser

echo.
echo [6/6] Starting server...
echo.
echo ========================================
echo    WeatherWise is running!
echo    Open: http://localhost:8000
echo ========================================
echo.
python manage.py runserver