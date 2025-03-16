from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import Player, TemperatureGameSession
from django.http import HttpResponse
# Create your views here.
def sign_in(request):
    if request.method == "GET":
        return render (request, "sign_in.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        player, created = Player.objects.get_or_create(username=username)
        return redirect('start_temp', player_id=player.id) # Will change this to game_selection screen

def start_game(request, player_id):
    if request.method == "GET":
        return render(request, "weather_game.html")
    player = get_object_or_404(Player, id=player_id)
    game = TemperatureGameSession.objects.create(player=player)
    pass # will redirect to prompt question in the future

# Utility Functions

def calculate_score(actual_temp, user_guess):
    error = abs(actual_temp - user_guess)
    return max(0, 250 - int(error * 10))

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
    return render(request, 'games/game_selection.html', {
        'player': player,
        'available_games': [
            {
                'id': 'temperature',
                'name': 'Temperature Guessing Game',
                'description': 'Guess the correct temperature and earn points!',
                'url': f'/temperature/?player_id={player_id}'
            },
            # Add more games here as we develop them
        ]
    })
