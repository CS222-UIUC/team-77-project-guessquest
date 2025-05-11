import requests
from . import models
from django.shortcuts import get_object_or_404
def create_trivia_game (player):
    game = models.TriviaGameSession.objects.create(player=player)
    question = game.create_question()
    return game, question
def store_trivia_session_data(request, player, game, question):
    request.session['game_id'] = game.id
    request.session['question_id'] = question.id
    request.session['player_id'] = player.id

def get_trivia_post_data(request):
    game_id = request.session.get('game_id')
    question_id = request.session.get('question_id')
    player_id = request.session.get('player_id')
    guess = int(request.POST.get('guess'))
    game = get_object_or_404(models.TemperatureGameSession, id=game_id)
    question = get_object_or_404(models.TemperatureQuestion, id=question_id)
    player = get_object_or_404(models.Player, id=player_id)
    return guess, player, game, question
def process_trivia_guess(game, question, guess):
    score = 0
    if guess == question.correct_answer:
        score += 10
    game.update_score(score)
    game.save()
    
def build_game_context(game, question):
    return {
        'score': game.score,
        'questions_left': game.questions_left,
        'question_text': question.question_text,
        'correct_answer': question.correct_answer,
        'incorrect_answers': question.incorrect_answers,
    }
