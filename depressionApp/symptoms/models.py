from django.db import models

# Create your models here.

class Questionnaire(models.Model):
    """Represents a symptom assessment questionnaire."""
    name = models.CharField(max_length=15)
    description = models.TextField()

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

    def __str__(self):
        return "{Questionnaire: " + self.questionnaire.name + ", Date: " + self.date + "}"
