import requests
from django.conf import settings
from . import models
import json
import random

# Global 
cities = [
    "New York", "Paris", "Tokyo", "London", "Los Angeles", "Bangkok", 
    "San Francisco", "Barcelona", "Shanghai", "Dubai", "Vienna", 
    "Rome", "Berlin", "Chicago", "Houston", "Phoenix", "Philadelphia", 
    "San Antonio", "San Diego", "Dallas", "Austin", "Seattle", 
    "Denver", "Boston", "Las Vegas"
]

class CityNotFoundError(Exception):
    pass
class CoordinatesNotFoundError(Exception):
    pass
def get_city_temperature(city) :
    lat,lon = city_to_coords(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=imperial"
    response = requests.get(url)
    if response.status_code != 200:
        raise CoordinatesNotFoundError(f"The coordinates, {lat}, {lon} was not found")
    data = response.json()
    return data["main"]["temp"]
def city_to_coords(city) :
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},&appid={settings.OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise CityNotFoundError(f"The city, {city} was not found")
    data = response.json()
    return data[0]["lat"], data[0]["lon"]
def get_random_city() :
    return random.choice(cities)
# Temperature scoring algorithm    
def calculate_score(actual_temp, user_guess):
    error = abs(actual_temp - user_guess)
    return max(0, 250 - int(error * 10))
def process_weather_guess(game, question, guess):
    score = calculate_score(question.actual_temperature, guess)
    game.update_score(score)
    game.save()
    