import requests
from django.conf import settings
from . import models
import json
import random
from django.shortcuts import get_object_or_404

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
def get_city_temperature(city, metric=False) :
    lat,lon = city_to_coords(city)
    units = 'metric' if metric else 'imperial'
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units={units}"
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
def calculate_score(actual_temp, user_guess):
    error = abs(actual_temp - user_guess)
    return max(0, 250 - int(error * 10))
def process_weather_guess(game, question, guess):
    score = calculate_score(question.actual_temperature, guess)
    game.update_score(score)
    game.save()
def create_weather_game(player):
    game = models.TemperatureGameSession.objects.create(player=player)
    question = game.create_question()
    return game, question
def store_weather_session_data(request, player, game, question):
    request.session['game_id'] = game.id
    request.session['question_id'] = question.id
    request.session['player_id'] = player.id
def store_weather_session_question(request, question):
    request.session['question_id'] = question.id
def get_weather_post_data(request):
    game_id = request.session.get('game_id')
    question_id = request.session.get('question_id')
    player_id = request.session.get('player_id')
    guess = int(request.POST.get('guess'))
    game = get_object_or_404(models.TemperatureGameSession, id=game_id)
    question = get_object_or_404(models.TemperatureQuestion, id=question_id)
    player = get_object_or_404(models.Player, id=player_id)
    return guess, player, game, question
def build_game_context(score, questions_left, city, actual_temperature):
    return {
            'score': score,
            'questionsNum': 5 - questions_left,
            'city': city,
            'actualTemperature' : actual_temperature
        }
