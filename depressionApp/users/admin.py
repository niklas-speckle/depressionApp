from django.contrib import admin
from .models import HealthProfessionalProfile, PatientProfile
# Register your models here.

admin.site.register([HealthProfessionalProfile, PatientProfile])