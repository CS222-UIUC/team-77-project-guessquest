from django.db import models
from django.utils.timezone import now
#TODO LEADERBOARD


class Player(models.Model):
    username = models.CharField(max_length=15)
    high_score = models.FloatField(default=0)
    
    def update_high_score(self, score):
        if score > self.high_score:
            self.score = score
        
    
    # returns username as a string
    def __str__(self):
        return self.username

class TemperatureGameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    questions_left = models.IntegerField(default=5)
    time_created = models.DateTimeField(auto_now_add=True)
    game_status = models.CharField(max_length=10, choices=[("active", "Active"), ("completed", "Completed")], default='active')
    
    def update_score(self, points):
        self.total_score += points
        self.questions_left -= 1
        if self.is_game_over():
            self.game_status = "completed"
        self.save()
        
    def is_game_over(self):
        return self.questions_left == 0
        
class TemperatureQuestion(models.Model):
    game = models.ForeignKey(TemperatureGameSession, related_name="questions", on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    user_guess = models.FloatField(null=False, blank=False)
    actual_temperature = models.FloatField(null=False, blank=False)
    time_created = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(default=30) # 30 seconds
    
    def __str__(self):
        return f"What is the current temperature of {self.city}?"
    
    def check_guess(self): # calculates and returns points
        #scoring algorithm subject to change
        error = abs(self.actual_temperature - self.user_guess)
        points = max(0, 250 - int(error * 10))
    
        return points