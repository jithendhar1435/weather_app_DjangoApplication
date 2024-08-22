from django.shortcuts import render, redirect
import requests
from django.utils import timezone
from datetime import timedelta
from .models import Cities, WeatherData

def weather_app(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=13f0f003817e71d5dd205b981c28cfc9'

    weather_data = []
    trend_data = {}
    alerts = []

    if request.method == 'POST':
        city_name = request.POST.get('city')
        if city_name:
            weather_data.clear()
            trend_data.clear()
            alerts.clear()

            
            city, created = Cities.objects.get_or_create(city=city_name)

         
            get_weather = requests.get(url.format(city_name)).json()
            weather = {
                'city': city.city,
                'temp': get_weather['main']['temp'],
                'humidity': get_weather['main']['humidity'],
                'wind_speed': get_weather['wind']['speed'],
                'desc': get_weather['weather'][0]['description'],
                'icon': get_weather['weather'][0]['icon'],
            }
            weather_data.append(weather)

            
            WeatherData.objects.create(
                city=city,
                temperature=weather['temp'],
                humidity=weather['humidity'],
                wind_speed=weather['wind_speed'],
                description=weather['desc'],
                icon=weather['icon']
            )

            past_24_hours = timezone.now() - timedelta(hours=24)
            recent_weather = WeatherData.objects.filter(city=city, timestamp__gte=past_24_hours)

            if recent_weather.exists():
                avg_temp = sum([data.temperature for data in recent_weather]) / recent_weather.count()
                avg_humidity = sum([data.humidity for data in recent_weather]) / recent_weather.count()

                trend_data[city.city] = {
                    'avg_temp': avg_temp,
                    'avg_humidity': avg_humidity
                }

       
            if weather['temp'] > 100 or weather['humidity'] > 90:
                alerts.append(f'Extreme weather alert for {city.city}: {weather["desc"]}')

            return render(request, 'weather/weather_page.html', {
                'weather_data': weather_data,
                'trend_data': trend_data,
                'alerts': alerts,
            })

    return render(request, 'weather/weather_page.html')
