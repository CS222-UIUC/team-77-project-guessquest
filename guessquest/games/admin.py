from django.contrib import admin
from .models import TriviaQuestion

# Register your models here.
@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'difficulty')    # whatever fields you have
    search_fields = ('question_text', 'difficulty')

