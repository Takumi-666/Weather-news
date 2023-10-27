from django.urls import path
from api.views import get_weather

urlpatterns = [
    path('get_weather/', get_weather, name='get_weather'),
]
