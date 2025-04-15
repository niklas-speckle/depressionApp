from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Questionnaire(models.Model):
    """Represents a symptom assessment questionnaire."""
    name = models.CharField(max_length=35, unique=True)
    description = models.TextField()

    slug = models.SlugField(unique=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Question(models.Model):
    """Represents a question in a questionnaire."""
    question = models.TextField()
    questionnaire = models.ForeignKey(Questionnaire, related_name="questions", on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class ResponseOption(models.Model):
    """Represents an answer option for a multiple-choice or scale question."""
    text = models.TextField()
    value = models.SmallIntegerField()
    question = models.ForeignKey(Question, related_name="response_options", on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class UserResponse(models.Model):
    """Stores responses from a user for a questionnaire."""
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    responses = models.ManyToManyField(ResponseOption)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "{Questionnaire: " + self.questionnaire.name + ", Date: " + str(self.date) + ", " + str(self.user) + "}"
    
    def get_score(self):
        score = 0
        for response in self.responses.all():
            score += response.value
        return score

