from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Player, TemperatureGameSession, TemperatureQuestion
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .trivia_services import TriviaService
from . import weather_services
from . import trivia_services

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
        feedback = True
        context = weather_services.build_game_context(game.score, game.questions_left, question.city, question.actual_temperature, feedback) 
        return render(request, "weatherGame.html", context)
    elif request.method == "POST":
        if 'guess' in request.POST:
            display_feedback = False
            guess, player, game, question = weather_services.get_weather_post_data(request)
            score = weather_services.process_weather_guess(game, question, guess)
            message = weather_services.get_message(score, guess, question.actual_temperature)
            context = weather_services.build_game_context(game.score, game.questions_left, question.city, question.actual_temperature, display_feedback, message)
            weather_services.store_weather_session_data(request, player, game, question, message)
            return render(request, "weatherGame.html", context)
        elif 'next' in request.POST:
            display_feedback = True
            player_id = request.session['player_id']
            game_id = request.session['game_id']
            player = Player.objects.get(id=player_id)
            game = TemperatureGameSession.objects.get(id=game_id)
            message = request.session['message']
            if game.no_questions_left():
                game.end_game()
                end = True
                top_ten = Player.objects.order_by('-weather_high_score')[:10]
                info = {'end': end, 'id' : player.id, 'top_ten': top_ten, 'final_score' : game.score}
                return render(request, f'weatherGame.html', info)
            next_question = game.create_question()
            weather_services.store_weather_session_data(request, player, game, next_question)
            context = weather_services.build_game_context(game.score, game.questions_left, next_question.city, next_question.actual_temperature, display_feedback, message) 
            return render(request, "weatherGame.html", context)
        
def trivia_game(request, player_id):
    if request.method == "GET":
        player = get_object_or_404(Player, id=player_id)
        game, question = trivia_services.create_trivia_game(player)
        trivia_services.store_trivia_session_data(request, player, game, question)
        context = trivia_services.build_game_context(game, question)
        return render(request, "triviaGame.html", context)
    elif request.method == "POST":
        player = get_object_or_404(Player, id=player_id)
        guess, player, game, question = trivia_services.get_trivia_post_data(request)
        trivia_services.process_trivia_guess(game, question, guess)
        if game.no_questions_left():
            game.end_game()
            top_ten = Player.objects.order_by('-trivia_high_score')[:10]
            return render(request, f'triviaLeaderBoard.html', {
                'top_ten' : top_ten,
                'final_score' : game.score
            })
        next_question = game.create_question()
        trivia_services.store_trivia_session_data(request, next_question)
        context = trivia_services.build_game_context(game, next_question)
        return render(request, "triviaGame.html", context)
        
    

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