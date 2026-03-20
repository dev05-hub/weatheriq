# Weatheriq

A weather forecasting web application built with Python Django and MySQL.

## Features
- User registration and login system
- Live weather data for any city worldwide
- 5-day weather forecast
- Temperature and humidity history charts
- Weather history saved in MySQL database
- User profile management
- Search history with clear option

## Tech Stack
| Technology | Purpose |
|---|---|
| Python 3.12 | Backend language |
| Django 6.0 | Web framework |
| MySQL 8.0 | Database |
| OpenWeatherMap API | Weather data |
| Chart.js | Data visualization |
| HTML CSS JavaScript | Frontend |

## How to Run
### 1. Clone the repository
```
git clone https://github.com/dev05-hub/weatheriq.git
cd weatheriq
```

### 2. Create virtual environment
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install packages
```
pip install -r requirements.txt
```

### 4. Setup configuration
```
copy .env.example .env
```
Then open `.env` and fill in your values.

### 5. Create MySQL database
```sql
CREATE DATABASE weatherwise_db;
```

### 6. Run migrations
```
python manage.py migrate
python manage.py createsuperuser
```

### 7. Start server
```
python manage.py runserver
```

### 8. Open browser
```
http://localhost:8000
```

## Pages
| Page | URL |
|---|---|
| Dashboard | / |
| Login | /auth/login/ |
| Register | /auth/register/ |
| Profile | /auth/profile/ |
| Admin | /admin/ |

## Configuration
Copy `.env.example` to `.env` and fill in:

| Variable | Where to get it |
|---|---|
| SECRET_KEY | Any random long string |
| DB_PASSWORD | Your MySQL password |
| OPENWEATHER_API_KEY | Free at openweathermap.org/api |

## Developer
- **Name:** Your Name
- **College:** Your College Name
- **GitHub:** https://github.com/dev05-hub