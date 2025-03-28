import requests
from django.conf import settings
import json

class CityNotFoundError(Exception):
    pass

def get_city_temperature(city) :
    # Dummy data for Champaign
    lat,lon = city_to_coords(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    if response.status_code != 200:
        raise CityNotFoundError(f"The city, {city} was not found")
    data = response.json()
    return data["main"]["temp"]
def city_to_coords(city) :
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},&appid={settings.OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise CityNotFoundError(f"The city, {city} was not found")
    data = response.json()
    return data[0]["lat"], data[0]["lon"]