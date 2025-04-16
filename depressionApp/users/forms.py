from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import USER_TYPE, PatientProfile, HealthProfessionalProfile, TherapyAgreement
from django.contrib.auth.models import User, Group
from django.db import transaction

@transaction.atomic
class RegisterUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPE, label="User Type", required=True)


    def save(self):
        new_user = super().save()
        user_type = self.cleaned_data.get('user_type')

        if user_type == USER_TYPE.HEALTH_PROFESSIONAL:
            profile = HealthProfessionalProfile(user=new_user)
            new_user.groups.add(Group.objects.get(name='Health-Professional'))
        elif user_type == USER_TYPE.PATIENT:
            profile = PatientProfile(user=new_user)
            new_user.groups.add(Group.objects.get(name='Patient'))
        else:
            raise ValueError("Invalid user type selected.")
        new_user.save()
        profile.save()
        return new_user

        
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')


class SearchPatientForm(forms.Form):
    patient_profile = forms.ModelChoiceField(label="Username", queryset=PatientProfile.objects, required=True)

    def save(self, health_professional_profile):

        patient_profile = self.cleaned_data.get('patient_profile')

        therapy_agreement = TherapyAgreement(
            health_professional=health_professional_profile,
            patient=patient_profile
        )

        therapy_agreement.save()

        return therapy_agreement


        