from django.contrib import admin
from .models import HealthProfessionalProfile, PatientProfile, TherapyAgreement

# Register your models here.

admin.site.register([HealthProfessionalProfile, PatientProfile, TherapyAgreement])