from django.contrib import admin
from .models import Questionnaire, Question, ResponseOption, UserResponse

# Register your models here.
admin.site.register([Question, Questionnaire, ResponseOption, UserResponse])