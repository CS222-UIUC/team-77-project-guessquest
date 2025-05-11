from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import Player, TemperatureGameSession, TemperatureQuestion
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import requests
from . import weather_services
# Create your views here.
def sign_in(request):
    if request.method == "GET":
        return render (request, "startScreen.html")
    elif request.method == "POST":
        username = request.POST.get("playername")
        player, created = Player.objects.get_or_create(username=username)
        return redirect(f'/games?player_id={player.id}')
def weather_game(request, player_id):
    if request.method == "GET":
        player = get_object_or_404(Player, id=player_id)
        game, question = weather_services.create_weather_game(player)
        weather_services.store_weather_session_data(request, player, game, question)
        info = weather_services.build_game_context(game.score, game.questions_left, question.city, question.actual_temperature, True) 
        return render(request, "weatherGame.html", info)
    elif request.method == "POST":
        if 'guess' in request.POST:
            guess = int(request.POST.get('guess'))
            player, game, question = weather_services.get_weather_post_data(request)
            score = weather_services.process_weather_guess(game, question, guess)
            feedback = weather_services.get_feedback(score, game.questions_left, question.actual_temperature, guess, False)
            return render(request, "weatherGame.html", feedback)
        elif 'next' in request.POST:
            player, game, question = weather_services.get_weather_post_data(request)
            if game.no_questions_left():
                game.end_game()
                end = True
                info = {'end': end, 'id' : player.id, 'final_score' : game.score}
                return render(request, "weatherGame.html", info)
            next_question = game.create_question()
            weather_services.store_weather_session_question(request, next_question)
            info = weather_services.build_game_context(game.score, game.questions_left, next_question.city, next_question.actual_temperature, True)
            return render(request, "weatherGame.html", info)

def leaderboard(request, player_id):
    if request.method == "GET":
        top_ten = Player.objects.order_by('-high_score')[:10]
        return render(request, 'leaderboard.html', {'id': player_id, 'leaderboard': top_ten})
    player = get_object_or_404(Player, id=player_id)

        
def trivia_game(request, player_id):
    if request.method == "GET":
        return render(request, "triviaGame.html", {'id': player_id})
    player = get_object_or_404(Player, id=player_id)

def spotify_game(request, player_id):
    if request.method == "GET":
        return render(request, "spotify_game.html")
    player = get_object_or_404(Player, id=player_id)


# view for game selection page
def game_selection(request):
    """
    View for the game selection screen.
    Displays available games for the player to choose from.
    """
    player_id = request.GET.get('player_id')
    
    if not player_id:
        return JsonResponse({"error": "Player ID is required"}, status=400)
    
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({"error": "Player not found"}, status=404)
    
    # Render the game selection template with player information
    return render(request, 'game_selection.html', {
        'player': player,
        'available_games': [
            {
                'id': 'temperature',
                'name': 'Weather Game',
                'description': 'Guess the correct temperature and earn points!',
                'image': 'css/selectionImages/weather.jpg',
                'url': f'/temperature/{player_id}'
            },
            {
                'id': 'trivia',
                'name': 'Trivia Game',
                'description': 'Trivia Game!',
                'image': 'css/selectionImages/trivia.jpg',
                'url': f'/trivia/{player_id}'
            }
        ]
    })
