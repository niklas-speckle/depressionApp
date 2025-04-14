from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HealthProfessionalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_professional_profile', unique=True)

    def __str__(self):
        return str(self.user)
    

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', unique=True)
    health_professional = models.ManyToManyField('HealthProfessionalProfile', related_name="patients", blank=True)

    def __str__(self):
        return str(self.user)