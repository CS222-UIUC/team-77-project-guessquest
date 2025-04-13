from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import Player, TemperatureGameSession, TemperatureQuestion
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .trivia_service import TriviaService
import random
import requests
from . import services
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
        game = TemperatureGameSession.objects.create(player=player)
        question = game.create_question()
        request.session['game_id'] = game.id
        request.session['question_id'] = question.id
        game.save()
        question.save()
        info = {
            'score': game.score,
            'questionNum': 5 - game.questions_left,
            'city': question.city,
            'actualTemperature': question.actual_temperature,
        }
        return render(request, "weatherGame.html", info)
    elif request.method == "POST":
        game_id = request.session.get('game_id')
        question_id = request.session.get('question_id')
        guess = int(request.POST.get('guess'))

        player = get_object_or_404(Player, id=player_id)
        game = get_object_or_404(TemperatureGameSession, id=game_id)
        question = get_object_or_404(TemperatureQuestion, id=question_id)
        
        services.process_weather_guess(game, question, guess)
        
        if game.no_questions_left():
            game.end_game()
            return redirect(f'/trivia/{player_id}')
        question = game.create_question()
        request.session['question_id'] = question.id
        game.save()
        question.save()
        info = {
            'score': game.score,
            'questionsNum': 5 - game.questions_left,
            'city': question.city,
            'actualTemperature' : question.actual_temperature
        }
        return render(request, "weatherGame.html", info)

def trivia_game(request, player_id):
    if request.method == "GET":
        return render(request, "triviaGame.html")
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
                'url': f'/temperature/{player_id}'
            },
            {
                'id': 'trivia',
                'name': 'Trivia Game',
                'description': 'Trivia Game!',
                'url': f'/trivia/{player_id}'
            },
            {
                'id': 'spotify',
                'name': 'Spotify Game',
                'description': 'Spotify Game!',
                'url': f'/spotify/{player_id}'
            }
        ]
    })

class TriviaAPIView(APIView):
    def get(self, request):
        # Get parameters from request
        amount = request.query_params.get('amount', 10)
        category = request.query_params.get('category', None)
        difficulty = request.query_params.get('difficulty', None)
        question_type = request.query_params.get('type', None)
        
        # Fetch questions from the service
        questions = TriviaService.get_questions(
            amount=amount, 
            category=category,
            difficulty=difficulty,
            question_type=question_type
        )
        
        return Response(questions)