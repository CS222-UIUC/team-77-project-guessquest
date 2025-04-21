from django.db import models
from django.utils.timezone import now
from . import weather_services
#TODO LEADERBOARD


class Player(models.Model):
    username = models.CharField(max_length=15)
    high_score = models.FloatField(default=0)
    
    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score

    # returns username as a string
    def __str__(self):
        return self.username

class TemperatureGameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    questions_left = models.IntegerField(default=5)
    time_created = models.DateTimeField(auto_now_add=True)
    game_status = models.CharField(max_length=10, choices=[("active", "Active"), ("completed", "Completed")], default='active')
    
    def create_question(self) :
        city = weather_services.get_random_city()
        actual_temperature = weather_services.get_city_temperature(city)
        question = TemperatureQuestion.objects.create(game=self, city=city, actual_temperature=actual_temperature)
        self.questions_left -= 1
        return question
    def get_latest_question(self):
        return self.questions.last()
    def update_score(self, points):
        self.score += points
    def end_game(self):
        self.game_status = "completed"
        self.player.update_high_score(self.score)
        self.save()
        self.player.save()
        self.delete()
    def no_questions_left(self):
        if self.questions_left == 0:
            self.game_status = 'completed'
        return self.questions_left == 0
        
class TemperatureQuestion(models.Model):
    game = models.ForeignKey(TemperatureGameSession, related_name="questions", on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    user_guess = models.FloatField(null=True, blank=True)
    actual_temperature = models.FloatField(null=False, blank=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=30) # 30 seconds
    
    def __str__(self):
        return f"What is the current temperature of {self.city}?"
    