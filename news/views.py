from django.conf import settings
from django.views.generic import TemplateView
import requests
from django.shortcuts import render
import os
from dotenv import load_dotenv

load_dotenv()

def weather_view(request):
    weather_data = {}
    exception_occurred = False

    # Handling POST requests for city-based weather search
    if request.method == 'POST':
        # Check if the form has city or geolocation data
        city = request.POST.get('city')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        api_key = os.getenv("WEATHER_API_KEY")  # Replace with your OpenWeatherMap API key

        # If city is provided
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city,
                    'temp': data['main']['temp'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'day': data['weather'][0]['main'],
                    'image_url': get_background_image_url(data['weather'][0]['main'])
                }
            else:
                exception_occurred = True

        # If geolocation (latitude and longitude) is provided
        elif latitude and longitude:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temp': data['main']['temp'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'day': data['weather'][0]['main'],
                    'image_url': get_background_image_url(data['weather'][0]['main'])
                }
            else:
                exception_occurred = True
        else:
            exception_occurred = True

    return render(request, 'index.html', {'exception_occurred': exception_occurred, **weather_data})

def get_background_image_url(weather_main):
    """Choose background image based on weather"""
    weather_backgrounds = {
        'Clear': 'https://images.pexels.com/photos/414659/pexels-photo-414659.jpeg',
        'Clouds': 'https://images.pexels.com/photos/158163/clouds-cloudporn-weather-lookup-158163.jpeg',
        'Rain': 'https://images.pexels.com/photos/459451/pexels-photo-459451.jpeg',
        'Snow': 'https://images.pexels.com/photos/2698519/pexels-photo-2698519.jpeg',
        'Thunderstorm': 'https://images.pexels.com/photos/1118869/pexels-photo-1118869.jpeg',
        'Drizzle': 'https://images.pexels.com/photos/459447/pexels-photo-459447.jpeg',
        'Mist': 'https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg'
    }
    return weather_backgrounds.get(weather_main, 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg')
