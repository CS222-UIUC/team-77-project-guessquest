from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from models import Player, TemperatureGameSession, TemperatureQuestion
from django.http import HttpResponse
import services
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if not username:
            return JsonResponse({"error": "Username not found."}, status=400)
        player, created = Player.objects.get_or_create(username=username)
        return redirect(f'/games?player_id={player.id}')

def start_game(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "GET":
        return render(request, "weather_game.html")
    elif request.method == "POST":
        game = TemperatureGameSession.objects.create(player=player)
        return JsonResponse({"game_id": game.id})

def get_next_question(request):
    game_id = request.POST.get("game_id")
    if not game_id:
        return JsonResponse({"error": "Missing Game ID"}, status=400)
    game = get_object_or_404(TemperatureGameSession, id=game_id)
    # will need to implement get random city logic. Hardcoding for now
    city = "Champaign"
    correct_temp = services.get_city_temperature()
    question = TemperatureQuestion.objects.create(city=city, game=game, actual_temperature=correct_temp)
    return JsonResponse({
        "city": city,
        "question_id": question.id
    })
    
def submit_guess(request):
    question_id = request.GET.get("question_id")
    if not question_id:
        return JsonResponse({"error" : "Question ID is missing"})
    guess = request.GET.get("guess")
    if not guess:
        return JsonResponse({"error": "User guess is missing"})
    question = get_object_or_404(TemperatureQuestion, id=question_id)
    
    question.user_guess = guess
    question.save()
    
    correct_temp = question.actual_temperature
    score = services.calculate_score(guess, correct_temp)
    
    game = question.game
    game.update_score(score)
    game.save()
    
    return JsonResponse({"correct_temp" : correct_temp, "score" : score, "total_score" : game.total_score,
                         "questions_left" : game.questions_left, "game_status" : game.game_status})
    
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
                'name': 'Temperature Guessing Game',
                'description': 'Guess the correct temperature and earn points!',
                'url': f'/temperature/?player_id={player_id}'
            },
            # Add more games here as we develop them
        ]
    })
