
import datetime
import requests
import threading
from django.shortcuts import render
from .forms import CityForm

API_KEY = open("API_KEY","r").read()
thread1_data = []
thread2_data = []

def get_weather_and_forecast(city, token, current_weather_url, forecast_url,container):
    response = requests.get(current_weather_url.format(city, token)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']

    forecast_response = requests.get(forecast_url.format(lat, lon, token)).json()

    weather_data = {"city": city,
                    "temperature": round(response['main']['temp'] - 273.15, 2),
                    "description": response['weather'][0]['description'],
                    "icon": response['weather'][0]['icon']

                    }
    daily_forecasts = []

    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']

        })

    container.append(weather_data, daily_forecasts)

def start(request):
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == "POST":

        city1 = request.POST['city1']
        city2 = request.POST.get('city2',None)

        if city1 and city2:

            task1 = threading.Thread(target=get_weather_and_forecast,args=(city1,API_KEY,current_weather_url,forecast_url,thread1_data))
            task2 = threading.Thread(target=get_weather_and_forecast,args=(city2,API_KEY,current_weather_url,forecast_url,thread2_data))

            task1.start()
            task2.start()


            task1.join()
            task2.join()

            context = {
                "form":CityForm(),
                "weather_data1": thread1_data[0],
                "daily_forecasts1": thread1_data[1],
                "weather_data2": thread2_data[0],
                "daily_forecasts2": thread2_data[1]
            }
            return render(request, "weather_app/start_page.html", context)

        else:
            task1 = get_weather_and_forecast(city1,API_KEY,current_weather_url,forecast_url,thread1_data)

            context = {
                "form": CityForm(),
                "weather_data1": thread1_data[0],
                "daily_forecasts1": thread1_data[1],
                "weather_data2": None,
                "daily_forecasts2": None
            }

            return render(request, "weather_app/start_page.html", context)

    else:
        return render(request, "weather_app/start_page.html", {"form":CityForm()})





