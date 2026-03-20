import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import City, WeatherRecord, ForecastRecord


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')


def get_weather(request):
    city_name = request.GET.get('city', 'Mumbai').strip()
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    data = response.json()

    if str(data.get('cod')) == '200':
        try:
            city, created = City.objects.get_or_create(
                name=data['name'],
                country_code=data['sys']['country'],
                defaults={
                    'latitude': data['coord']['lat'],
                    'longitude': data['coord']['lon'],
                }
            )
            WeatherRecord.objects.create(
                city=city,
                user=request.user if request.user.is_authenticated else None,
                temperature=round(data['main']['temp'], 1),
                feels_like=round(data['main']['feels_like'], 1),
                temp_min=round(data['main']['temp_min'], 1),
                temp_max=round(data['main']['temp_max'], 1),
                humidity=data['main']['humidity'],
                pressure=data['main']['pressure'],
                visibility=data.get('visibility', 0),
                wind_speed=round(data['wind']['speed'] * 3.6, 1),
                wind_deg=data['wind'].get('deg', 0),
                cloudiness=data['clouds']['all'],
                condition=data['weather'][0]['main'],
                condition_description=data['weather'][0]['description'],
                rain_1h=data.get('rain', {}).get('1h', 0),
            )
            print(f"✅ Saved: {data['name']} — {data['main']['temp']}°C")
        except Exception as e:
            print(f"❌ Save error: {e}")

    return JsonResponse(data)


def get_forecast(request):
    city_name = request.GET.get('city', 'Mumbai').strip()
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city_name,
        'appid': settings.OPENWEATHER_API_KEY,
        'units': 'metric',
        'cnt': 40,
    }
    response = requests.get(url, params=params)
    data = response.json()

    daily = {}
    for item in data.get('list', []):
        date = item['dt_txt'].split(' ')[0]
        time = item['dt_txt'].split(' ')[1]
        if time == '12:00:00' and date not in daily:
            daily[date] = {
                'date': date,
                'temp_max': round(item['main']['temp_max']),
                'temp_min': round(item['main']['temp_min']),
                'temp': round(item['main']['temp']),
                'humidity': item['main']['humidity'],
                'wind': round(item['wind']['speed'] * 3.6),
                'condition': item['weather'][0]['main'],
                'condition_desc': item['weather'][0]['description'],
                'pop': round(item.get('pop', 0) * 100),
            }

    return JsonResponse({'forecast': list(daily.values())[:5]})


def get_chart_data(request):
    city_name = request.GET.get('city', 'Mumbai')
    try:
        city = City.objects.filter(name__icontains=city_name).first()
        if not city:
            return JsonResponse({'labels': [], 'temps': [], 'humidity': []})

        records = WeatherRecord.objects.filter(
            city=city
        ).order_by('-recorded_at')[:10]
        records = list(reversed(records))

        return JsonResponse({
            'labels': [r.recorded_at.strftime('%d %b %H:%M') for r in records],
            'temps': [r.temperature for r in records],
            'humidity': [r.humidity for r in records],
            'feels_like': [r.feels_like for r in records],
            'city': city.name,
        })
    except Exception as e:
        print(f"Chart error: {e}")
        return JsonResponse({'labels': [], 'temps': [], 'humidity': []})


def weather_history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    records = WeatherRecord.objects.filter(
        user=request.user
    ).select_related('city').order_by('-recorded_at')[:20]

    history = [{
        'city': r.city.name,
        'country': r.city.country_code,
        'temperature': r.temperature,
        'condition': r.condition_description,
        'humidity': r.humidity,
        'wind_speed': r.wind_speed,
        'recorded_at': r.recorded_at.strftime('%d %b %Y, %H:%M'),
    } for r in records]

    return JsonResponse({'history': history})