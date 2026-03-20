from django.db import models
from django.conf import settings


class City(models.Model):
    """Stores cities that have been searched."""
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cities'
        unique_together = ('name', 'country_code')
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.name}, {self.country_code}"


class WeatherRecord(models.Model):
    """Stores every weather search result in MySQL."""
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='records')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='weather_searches'
    )
    # Temperature
    temperature = models.FloatField()
    feels_like = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    # Atmosphere
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    visibility = models.IntegerField(null=True, blank=True)
    # Wind
    wind_speed = models.FloatField()
    wind_deg = models.IntegerField(default=0)
    # Sky
    cloudiness = models.IntegerField(default=0)
    condition = models.CharField(max_length=100)
    condition_description = models.CharField(max_length=200)
    # Rain
    rain_1h = models.FloatField(default=0)
    # Timestamp
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weather_records'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['city', '-recorded_at']),
        ]

    def __str__(self):
        return f"{self.city} — {self.temperature}°C at {self.recorded_at:%d %b %Y %H:%M}"


class ForecastRecord(models.Model):
    """Stores 5-day forecast data per city."""
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='forecasts')
    forecast_date = models.DateField()
    temp_max = models.FloatField()
    temp_min = models.FloatField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    condition = models.CharField(max_length=100)
    condition_description = models.CharField(max_length=200)
    rain_probability = models.IntegerField(default=0)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'forecast_records'
        unique_together = ('city', 'forecast_date')
        ordering = ['forecast_date']

    def __str__(self):
        return f"{self.city} forecast for {self.forecast_date}"