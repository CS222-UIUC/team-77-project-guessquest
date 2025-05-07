import requests
from django.conf import settings
from . import models
import json
import random
from django.shortcuts import get_object_or_404
import math

# Global 
cities = [
    "New York", "Paris", "Tokyo", "London", "Los Angeles", "Bangkok", 
    "San Francisco", "Barcelona", "Shanghai", "Dubai", "Vienna", 
    "Rome", "Berlin", "Chicago", "Houston", "Phoenix", "Philadelphia", 
    "San Antonio", "San Diego", "Dallas", "Austin", "Seattle", 
    "Denver", "Boston", "Las Vegas"
]

# Scoring
MAXSCORE = 100
# Message feedback
perfectGuess = ["Perfect", "Your luck is incredible", "Now that's a GUESS"]
goodGuess = ["Nice Guess", "That was close", "How did you know?", "Cool", "Awesome"]
badGuess = ["You can guess better", "Better luck next time", "Not even close"]
perfectGif = ['css/gifs/perfect/1.gif', 'css/gifs/perfect/2.gif', 'css/gifs/perfect/3.gif']
goodGif = ['css/gifs/good/1.gif', 'css/gifs/good/2.gif', 'css/gifs/good/3.gif']
badGif = ['css/gifs/bad/1.gif', 'css/gifs/bad/2.gif', 'css/gifs/bad/3.gif']

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
    sigma = 7  # higher sigma -> less drop off
    score = int(100 * math.exp(-(error**2) / (2 * sigma**2)))
    return int(score)
def process_weather_guess(game, question, guess):
    score = calculate_score(question.actual_temperature, guess)
    game.update_score(score)
    game.save()
    return score
def create_weather_game(player):
    game = models.TemperatureGameSession.objects.create(player=player)
    question = game.create_question()
    return game, question
def store_weather_session_data(request, player, game, question, message=None):
    request.session['game_id'] = game.id
    request.session['question_id'] = question.id
    request.session['player_id'] = player.id
    if message is not None:
        request.session['message'] = message
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
    
def build_game_context(score, questions_left, city, actual_temperature, display_feedback, message=None):
    context = {
            'score': score,
            'questionsNum': 5 - questions_left,
            'city': city,
            'actualTemperature' : actual_temperature,
            'feedback' : display_feedback
        }
    if message is not None:
        context['message'] = message['message']
        context['gif'] = message['gif']
    return context

def get_message(score, user_guess, actual_temperature):
    statistics = f'the actual temperature was {actual_temperature}°, you guessed {user_guess}°.'
    difference = abs(actual_temperature - user_guess)
    message = ""
    if (difference < 1):
        message = random.choice(perfectGuess)
        gif = random.choice(perfectGif)
    elif(difference <= 5):
        message = random.choice(goodGuess)
        gif = random.choice(goodGif)
    else:
        message = random.choice(badGuess)
        gif = random.choice(badGif)
    message += statistics
    return {'message': message,
            'gif': gif
    }

