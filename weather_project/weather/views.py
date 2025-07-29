import requests
from django.shortcuts import render
from .forms import CityForm

def get_weather_data(city):
    api_key = 'f3cee02c76408b8033f4240164452476'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return {'error': 'City not found'}
    else:
        return None

def index(request):
    weather_data = None
    form = CityForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        city = form.cleaned_data['city']
        weather_data = get_weather_data(city)
        if weather_data is None:
            form.add_error('city', 'Could not retrieve weather data. Please try again.')
        elif 'error' in weather_data:
            form.add_error('city', weather_data['error'])

    return render(request, 'index.html', {
        'form': form,
        'weather_data': weather_data if weather_data and 'error' not in weather_data else None
    })
