from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterUserForm, SearchPatientForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .permissionService import is_allowed_to_see_all_patients
from .models import PatientProfile, HealthProfessionalProfile, TherapyAgreement
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
import json


# Create your views here.

def register_view(request):
    # if user submits form, save the user to DB
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid:
            login(request, form.save())
            return redirect("symptoms:dashboard")
        
    form = RegisterUserForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("symptoms:dashboard")
    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    
@login_required(login_url="users:login")
def get_patients_list(request):
    current_user = request.user
    if is_allowed_to_see_all_patients(current_user):
        users = PatientProfile.objects.select_related('user').values_list('user__username', flat=True)
        return JsonResponse(list(users), safe=False)
    else:
        return HttpResponseForbidden("You do not have permission to view this user's responses.")
    
@login_required(login_url="users:login")
def create_therapy_agreement(request):
    if request.method == "POST":
        form = SearchPatientForm(data=request.POST)
        if form.is_valid():
            health_professional_profile = HealthProfessionalProfile.objects.get(user=request.user)
            therapy_agreement = form.save(health_professional_profile)
            print(therapy_agreement)
            return redirect("symptoms:dashboard")
    else: 
        form = SearchPatientForm(request.GET or None)
        return render(request, "users/create_therapy_agreement.html", {"form": form})
    
def your_therapists_view(request):
    """View to display the therapists of a single user."""
    current_user = request.user
    if current_user.groups.filter(name="Patient").exists():
        patient_profile_current_user = PatientProfile.objects.get(user = current_user)
        therapy_agreements = TherapyAgreement.objects.filter(patient=patient_profile_current_user, status=TherapyAgreement.STATUS.PENDING)
        therapists = patient_profile_current_user.health_professional.all()
        return render(request, 'users/your_therapists.html', {'therapists': therapists, 'therapy_agreements': therapy_agreements})
    else:
        return HttpResponseForbidden("You do not have permission to view this user's responses.")

@require_POST 
def set_therapy_agreement_status(request, therapy_agreement_id):
    new_status = json.loads(request.body).get("status")
    print("#############################################################")
    print(new_status)
    print("#############################################################")

    if new_status not in TherapyAgreement.STATUS.values:
        return HttpResponseBadRequest("Invalid status")
    
    try:
        therapy_agreement = TherapyAgreement.objects.get(id=therapy_agreement_id)
        therapy_agreement.status = new_status
        therapy_agreement.save()
        return JsonResponse({"status": "success"})
    except TherapyAgreement.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Therapy agreement not found"}, status=404)

