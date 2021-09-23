from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import requests

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=<API_KEY>"
        r = requests.get(url.format(city)).json()

        city_weather = {
            'id':city.id,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)

def delete(request, id):
    if request.method == 'POST':
        print(request)
        City.objects.filter(id=id).delete()
    return redirect('/')