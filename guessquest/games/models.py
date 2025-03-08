from django.db import models

# Create your models here.
class TemperatureGame(models.Model):
    total_score = models.IntegerField(default=0)
    questions_left = models.IntegerField(default=5)
    
        
class TemperatureQuestion(models.Model):
    game = models.ForeignObject(TemperatureGame, related_name="questions")
    city = models.CharField(max_length=50)
    user_guess = models.FloatField(null=True, blank=True)
    actual_temparature = models.FloatField(null=False, blank=False)
    time_limit = models.IntegerField(default=30) # 30 seconds
    
    