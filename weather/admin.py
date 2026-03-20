from django.contrib import admin
from .models import City, WeatherRecord, ForecastRecord


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_code', 'latitude', 'longitude', 'created_at']
    search_fields = ['name', 'country_code']


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ['city', 'user', 'temperature', 'condition', 'humidity', 'wind_speed', 'recorded_at']
    list_filter = ['condition', 'city__country_code']
    search_fields = ['city__name']
    ordering = ['-recorded_at']


@admin.register(ForecastRecord)
class ForecastRecordAdmin(admin.ModelAdmin):
    list_display = ['city', 'forecast_date', 'temp_min', 'temp_max', 'condition', 'rain_probability']
    search_fields = ['city__name']
    ordering = ['forecast_date']
