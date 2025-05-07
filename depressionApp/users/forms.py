from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import USER_TYPE, PatientProfile, HealthProfessionalProfile, TherapyAgreement
from django.contrib.auth.models import User, Group
from django.db import transaction

@transaction.atomic
class RegisterUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPE, label="User Type", required=True, widget=forms.Select(attrs={'class': 'form-dropdown'}))


    def save(self, commit=True):
        new_user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')

        if commit:
            new_user.save()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-textbox'})
        self.fields['password1'].widget.attrs.update({'class': 'form-textbox'})
        self.fields['password2'].widget.attrs.update({'class': 'form-textbox'})

    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')


class TherapyAgreementRequestForm(forms.Form):
    patient_profile = forms.ModelChoiceField(label="Username", queryset=PatientProfile.objects, required=True)

    def save(self, health_professional_profile):

        patient_profile = self.cleaned_data.get('patient_profile')

        if TherapyAgreement.objects.filter(health_professional=health_professional_profile, patient=patient_profile).exists():
            raise forms.ValidationError("Therapy agreement already exists for this patient.")

        therapy_agreement = TherapyAgreement(
            health_professional=health_professional_profile,
            patient=patient_profile
        )

        therapy_agreement.save()

        return therapy_agreement


        