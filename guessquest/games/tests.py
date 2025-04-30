from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import json
from .models import Player, TemperatureGameSession, TemperatureQuestion, TriviaGameSession, TriviaQuestion
from . import weather_services, trivia_services

class PlayerModelTests(TestCase):
    def test_create_player(self):
        """Test creating a player and default values"""
        player = Player.objects.create(username="testuser")
        self.assertEqual(player.username, "testuser")
        self.assertEqual(player.weather_high_score, 0)
        self.assertEqual(str(player), "testuser")

    def test_update_weather_high_score_higher(self):
        """Test updating high score with a higher value"""
        player = Player.objects.create(username="testuser", weather_high_score=100)
        player.update_weather_high_score(150)
        self.assertEqual(player.weather_high_score, 150)

    def test_update_weather_high_score_lower(self):
        """Test updating high score with a lower value (should not change)"""
        player = Player.objects.create(username="testuser", weather_high_score=100)
        player.update_weather_high_score(50)
        self.assertEqual(player.weather_high_score, 100)
        
    def test_update_trivia_high_score_higher(self):
        """Test updating trivia high score with a higher value"""
        player = Player.objects.create(username="testuser", trivia_high_score=50)
        player.update_trivia_high_score(75)
        self.assertEqual(player.trivia_high_score, 75)

    def test_update_trivia_high_score_lower(self):
        """Test updating trivia high score with a lower value (should not change)"""
        player = Player.objects.create(username="testuser", trivia_high_score=50)
        player.update_trivia_high_score(25)
        self.assertEqual(player.trivia_high_score, 50)
        
    def test_delete_player(self):
        """Test deleting a player"""
        player = Player.objects.create(username="testuser")
        player_id = player.id
        player.delete()
        
        # Makes sure the player is deleted
        self.assertFalse(Player.objects.filter(id=player_id).exists())
class TemperatureGameSessionTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(username="testuser")
        
    def test_create_game_session(self):
        """Test creating a game session with default values"""
        game = TemperatureGameSession.objects.create(player=self.player)
        self.assertEqual(game.player.username, "testuser")
        self.assertEqual(game.score, 0)
        self.assertEqual(game.questions_left, 5)
        self.assertEqual(game.game_status, "active")

    def test_update_score(self):
        """Test updating score and questions_left"""
        game = TemperatureGameSession.objects.create(player=self.player)
        game.update_score(100)
        self.assertEqual(game.score, 100)
        self.assertEqual(game.game_status, "active")

    def test_game_over(self):
        """Test that game status changes when no questions are left"""
        game = TemperatureGameSession.objects.create(player=self.player, questions_left=1)
        game.update_score(100)
        game.questions_left -= 1
        self.assertTrue(game.no_questions_left)
        self.assertEqual(game.score, 100)
        self.assertEqual(game.questions_left, 0)
        game.end_game()
        self.assertEqual(game.game_status, "completed")

    def test_no_questions_left(self):
        """Test the no_questions_left method"""
        game = TemperatureGameSession.objects.create(player=self.player)
        self.assertFalse(game.no_questions_left())
        
        game.questions_left = 0
        self.assertTrue(game.no_questions_left())
class TemperatureScoreCalculation(TestCase):
    def setUp(self):
        self.player = Player.objects.create(username="testuser")
        self.game = TemperatureGameSession.objects.create(player=self.player)
        
    def test_perfect_guess(self):
        actual_temperature = 30
        user_guess = 30
        points = weather_services.calculate_score(actual_temperature, user_guess)
        self.assertEqual(points, weather_services.MAXSCORE)
        
    def test_close_guess(self):
        actual_temperature = 30
        user_guess = 29
        points = weather_services.calculate_score(actual_temperature, user_guess)
        difference = abs(points - weather_services.MAXSCORE)
        self.assertTrue(difference < 3)
        
        user_guess = 28
        points = weather_services.calculate_score(actual_temperature, user_guess)
        missed_points = abs(points - weather_services.MAXSCORE)
        self.assertTrue(missed_points < 15)
        
        user_guess = 25
        points = weather_services.calculate_score(actual_temperature, user_guess)
        missed_points = abs(points - weather_services.MAXSCORE)
        self.assertTrue(missed_points < 30)
        
    def far_guess(self):
        actual_temperature = 30
        user_guess = 10
        points = weather_services.calculate_score(actual_temperature, user_guess)
        self.assertTrue(points < 10)
        
        actual_temperature = 30
        user_guess = 20
        points = weather_services.calculate_score(actual_temperature, user_guess)
        self.assertTrue(points < 10)
        
        actual_temperature = 30
        user_guess = 500
        points = weather_services.calculate_score(actual_temperature, user_guess)
        self.assertTrue(points == 0)
        
        actual_temperature = 30
        user_guess = -500
        points = weather_services.calculate_score(actual_temperature, user_guess)
        self.assertTrue(points == 0)
class TemperatureQuestionTests(TestCase):
    def setUp(self):
        self.player = Player.objects.create(username="testuser")
        self.game = TemperatureGameSession.objects.create(player=self.player)
        
    def test_create_question(self):
        """Test creating a temperature question"""
        question = TemperatureQuestion.objects.create(
            game=self.game,
            city="New York",
            user_guess=75.0,
            actual_temperature=72.5,
        )
        self.assertEqual(question.city, "New York")
        self.assertEqual(question.user_guess, 75.0)
        self.assertEqual(question.actual_temperature, 72.5)
        self.assertEqual(str(question), "What is the current temperature of New York?")

    def test_check_guess_perfect(self):
        """Test points calculation for a perfect guess"""
        question = TemperatureQuestion.objects.create(
            game=self.game,
            city="New York",
            user_guess=75.0,
            actual_temperature=75.0
        )
        points = weather_services.calculate_score(question.actual_temperature, question.user_guess)
        self.assertEqual(points, 100)

    def test_check_guess_close(self):
        """Test points calculation for a close guess"""
        question = TemperatureQuestion.objects.create(
            game=self.game,
            city="New York",
            user_guess=75.0,
            actual_temperature=72.5
        )
        points = weather_services.calculate_score(question.actual_temperature, question.user_guess)
        self.assertTrue(points < weather_services.MAXSCORE)
        self.assertTrue(weather_services.MAXSCORE - points < 10)  #should be close to max score
        
    def test_check_guess_far(self):
        """Test points calculation for a far guess"""
        question = TemperatureQuestion.objects.create(
            game=self.game,
            city="New York",
            user_guess=95.0,
            actual_temperature=65.0
        )
        points = weather_services.calculate_score(question.actual_temperature, question.user_guess)
        self.assertEqual(points, 0)
        question.user_guess = 85.0
        points = weather_services.calculate_score(question.actual_temperature, question.user_guess)

    def test_check_guess_negative_error(self):
        """Test points calculation when guess is lower than actual is equal to when guess is higher"""
        question = TemperatureQuestion.objects.create(
            game=self.game,
            city="New York",
            user_guess=65.0,
            actual_temperature=70.0
        )
        points = weather_services.calculate_score(question.actual_temperature, question.user_guess)
        self.assertTrue(points > 0 & points < weather_services.MAXSCORE)
        # Swap actual temperature and user guess
        points_swapped = weather_services.calculate_score(question.user_guess, question.actual_temperature)
        self.assertTrue(points == points_swapped)

class ViewsTests(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()
        # Create a test player
        self.test_player = Player.objects.create(username="testuser", weather_high_score=100)
        
    def test_sign_in_get(self):
        """Test GET request to sign_in view"""
        response = self.client.get(reverse('sign_in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'startScreen.html')
        
    def test_start_weather_game_get(self):
        """Test GET request to start_game view"""
        response = self.client.get(
            reverse('weather_game', kwargs={'player_id': self.test_player.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weatherGame.html')
        
    def test_sign_in_existing_user(self):
        """Test signing in with an existing username does not create a new player"""
        response = self.client.post(reverse('sign_in'), {'playername': 'testuser'})
        self.assertEqual(response.status_code, 302) # redirects
        
        # Ensure no new player is created
        player_count = Player.objects.filter(username='testuser').count()
        self.assertEqual(player_count, 1)
        
    def test_sign_in_new_user(self):
        """Test signing in with an new username creates a new player"""
        initial_player_count = Player.objects.count()
        response = self.client.post(reverse('sign_in'), {'playername': 'newuser'})
        self.assertEqual(response.status_code, 302)  # redirects

        # Ensure a new player is created
        player_count = Player.objects.filter(username='newuser').count()
        self.assertEqual(player_count, 1)

        # Ensure total player count increases by 1
        self.assertEqual(Player.objects.count(), initial_player_count + 1)
        
    def test_game_selection_missing_player_id(self):
        """Test game_selection view without player_id"""
        response = self.client.get(reverse('game_selection'))
        self.assertEqual(response.status_code, 400)
        
        # Check error message
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Player ID is required')
        
    def test_game_selection_invalid_player_id(self):
        """Test game_selection view with invalid player_id"""
        response = self.client.get(
            reverse('game_selection') + '?player_id=999'
        )
        self.assertEqual(response.status_code, 404)
        
        # Check error message
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Player not found')
        
class WeatherGameProcessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.player = Player.objects.create(username="testuser")
        self.game = TemperatureGameSession.objects.create(player=self.player)

    def test_full_game_process(self):
        """Test the entire weather game process"""
        # Step 1: Start the game
        response = self.client.get(reverse('weather_game', kwargs={'player_id': self.player.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weatherGame.html')

        # Step 2: Create a question
        question = self.game.create_question()
        # override with mock data
        question.city = "New York"
        question.user_guess = 75.0
        question.actual_temperature = 72.5
        question.save()

        self.assertEqual(question.city, "New York")
        self.assertEqual(question.user_guess, 75.0)
        self.assertEqual(question.actual_temperature, 72.5)

        # Step 3: Calculate score for the question
        points = weather_services.process_weather_guess(self.game, question, question.user_guess)
        self.assertTrue(points > 0)
        self.assertTrue(points < weather_services.MAXSCORE)

        # Step 4: Check game updates
        self.assertEqual(self.game.score, points)
        self.assertEqual(self.game.questions_left, 4)

        # Step 5: Check if game ends when no questions are left
        self.game.questions_left = 0
        self.assertTrue(self.game.no_questions_left())
        self.game.end_game()
        self.assertEqual(self.game.game_status, "completed")

    def test_game_restart(self):
        """Test restarting a completed game"""
        self.game.questions_left = 0
        self.game.end_game()
        self.assertEqual(self.game.game_status, "completed")

        # Restart the game
        new_game = TemperatureGameSession.objects.create(player=self.player)
        self.assertEqual(new_game.player, self.player)
        self.assertEqual(new_game.score, 0)
        self.assertEqual(new_game.questions_left, 5)
        self.assertEqual(new_game.game_status, "active")

class TestGetWeatherMessage(TestCase):
    def test_perfect_guess(self):
        score = weather_services.MAXSCORE
        user_guess = 25
        actual_temperature = 25
        expected_message = f"Perfect Guess<br>the actual temperature was {actual_temperature}°, you guessed {user_guess}°."
        self.assertEqual(weather_services.get_message(score, user_guess, actual_temperature), expected_message)

    def test_good_guess(self):
        score = int(weather_services.MAXSCORE * 0.8)
        user_guess = 30
        actual_temperature = 28
        expected_message = f"Good Guess<br>the actual temperature was {actual_temperature}°, you guessed {user_guess}°."
        self.assertEqual(weather_services.get_message(score, user_guess, actual_temperature), expected_message)

    def test_keep_guessing(self):
        score = int(weather_services.MAXSCORE * 0.5)
        user_guess = 30
        actual_temperature = 15
        expected_message = f"Keep Guessing<br>the actual temperature was {actual_temperature}°, you guessed {user_guess}°."
        self.assertEqual(weather_services.get_message(score, user_guess, actual_temperature), expected_message)
    
class TestTriviaServices(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()
        # Create a test player
        self.player = Player.objects.create(username="testuser", trivia_high_score=50)
        player = self.player
        # Mock data
        TriviaQuestion.objects.create(
        question_text="What is 2+2?",
        correct_answer="4",
        incorrect_answers=["3", "5", "22"],
        difficulty="easy",
        question_type="multiple"
        )
        
    def test_create_trivia_game(self):
        game, question = trivia_services.create_trivia_game(self.player)
        self.assertIsInstance(game, TriviaGameSession) # Ensures game is it's own instance
        self.assertIsNotNone(question)
        self.assertEqual(question.correct_answer, '4')
        self.assertEqual(len(question.incorrect_answers), 3)
        self.assertIn('3', question.incorrect_answers)
    def test_process_trivia_guess(self):
        game, question = trivia_services.create_trivia_game(self.player)
        guess = '22' # incorrect
        trivia_services.process_trivia_guess(game, question, guess)
        self.assertEqual(game.score, 0) # should stay the same
        guess = '4' # correct
        trivia_services.process_trivia_guess(game, question, guess)
        self.assertEqual(game.score, 10) # should be incrememented by 10
        guess = '5' # incorrect
        trivia_services.process_trivia_guess(game, question, guess)
        self.assertEqual(game.score, 10) # should stay the same

class TestTriviaModels(TestCase):
    def setUp(self):
        self.client = Client()
        self.player = Player.objects.create(username="testuser", trivia_high_score=0)
        TriviaQuestion.objects.create(
            question_text="What is the capital of France?",
            correct_answer="Paris",
            incorrect_answers=["London", "Berlin", "Madrid"],
            difficulty="medium",
            question_type="multiple"
        )
        self.game = TriviaGameSession.objects.create(player=self.player)
        self.initial_questions_left = self.game.questions_left
        self.assertEquals(self.initial_questions_left, 5)
    def test_create_question(self):
        question = self.game.create_question()
        self.assertFalse(self.game.no_questions_left())
        self.assertEqual(question.question_text, "What is the capital of France?")
        self.assertEqual(question.correct_answer, "Paris")
        self.assertEqual(len(question.incorrect_answers), 3)
        self.assertIn("London", question.incorrect_answers)
        self.assertEqual(question.difficulty, "medium")
        self.assertEqual(question.question_type, "multiple")
        self.assertEquals(self.game.questions_left, 4)
        question = self.game.create_question()
        question = self.game.create_question()
        question = self.game.create_question()
        self.assertFalse(self.game.no_questions_left())
        question = self.game.create_question()
        self.assertTrue(self.game.no_questions_left()) # should be out of questions
    
    def test_game_over(self):
        self.game.questions_left = 1
        self.game.score = 10
        self.game.decrement_question_count()
        self.assertEqual(self.game.game_status, "completed")
        self.assertEqual(self.game.questions_left, 0)
        self.assertTrue(self.game.game_over())
        self.assertEqual(self.player.trivia_high_score, 10) # updated player leaderboard
        
        self.assertFalse(TriviaGameSession.objects.filter(id=self.game.id).exists()) # Game is deleted from db
    