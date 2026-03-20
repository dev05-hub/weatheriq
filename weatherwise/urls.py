from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),
    path('auth/', include('users.urls')),
    path('alerts/', include('alerts.urls')),
]