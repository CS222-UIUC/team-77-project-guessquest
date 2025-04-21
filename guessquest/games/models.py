from django.db import models
from . import weather_services
#TODO LEADERBOARD


class Player(models.Model):
    username = models.CharField(max_length=15)
    weather_high_score = models.FloatField(default=0)
    trivia_high_score = models.FloatField(default=0)
    
    def update_weather_high_score(self, score):
        if score > self.weather_high_score:
            self.weather_high_score = score
            self.save()
    def update_trivia_high_score(self, score):
        if score > self.trivia_high_score:
            self.trivia_high_score = score
            self.save()
    # returns username as a string
    def __str__(self):
        return self.username


class BaseGameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    questions_left = models.IntegerField(default=5)
    game_status = models.CharField(max_length=10, choices=[("active", "Active"), ("completed", "Completed")], default='active')
    
    class Meta:
        abstract = True
    
    def update_score(self, points):
        self.score += points
        self.save()
    
    def end_game(self):
        self.game_status = "completed"
        self.save()
    def create_question(self) :
        self.questions_left -= 1
        self.save()
    def no_questions_left(self):
        return self.questions_left == 0
    
class TemperatureGameSession(BaseGameSession):
    def create_question(self) :
        super().create_question()
        city = weather_services.get_random_city()
        actual_temperature = weather_services.get_city_temperature(city)
        question = TemperatureQuestion.objects.create(game=self, city=city, actual_temperature=actual_temperature)
        return question
    def get_latest_question(self):
        return self.questions.last()
    
    def end_game(self):
        super().end_game()
        self.player.update_weather_high_score(self.score)
        self.delete()
        
        
class TemperatureQuestion(models.Model):
    game = models.ForeignKey(TemperatureGameSession, related_name="questions", on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    user_guess = models.FloatField(null=True, blank=True)
    actual_temperature = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return f"What is the current temperature of {self.city}?"

class TriviaGameSession(BaseGameSession):
    def create_question(self):
        super().create_question()
        return TriviaQuestion.objects.order_by('?').first()

class TriviaQuestion(models.Model):
    DIFFICULTY_CHOICES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    QUESTION_TYPE = [('multiple', 'Multiple Choice'), ('boolean', 'Boolean')]

    question_text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE, null=True, blank=True)
    correct_answer = models.CharField(max_length=50, null=True, blank=True)
    incorrect_answers = models.JSONField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.question_text} ({self.difficulty})"
