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
        return redirect('start_temp', player_id=player.id)

def start_game(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    game = TemperatureGameSession.objects.create(player=player)
    return JsonResponse({"game_id" : game.id})

# Utility Functions

def calculate_score(actual_temp, user_guess):
    error = abs(actual_temp - user_guess)
    return max(0, 250 - int(error * 10))
