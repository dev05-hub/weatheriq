from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/weather/', views.get_weather, name='get_weather'),
    path('api/forecast/', views.get_forecast, name='get_forecast'),
    path('api/chart/', views.get_chart_data, name='get_chart_data'),
    path('api/history/', views.weather_history, name='weather_history'),
]