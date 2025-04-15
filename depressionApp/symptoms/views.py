
from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Question, UserResponse
from .view_models.questionnaire import QuestionResponseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from users.models import HealthProfessionalProfile, PatientProfile
from django.http import HttpResponseForbidden
from users.permissionService import is_allowed_to_read

# Create your views here.

@login_required(login_url="/users/login")
def dashboard(request):

    current_user = request.user

    if current_user.groups.filter(name="Patient").exists():
        patient_profile_current_user = PatientProfile.objects.get(user = current_user)
        return user_responses_view(request, patient_profile_current_user)
        # questionnaires = Questionnaire.objects.all()
        # return render(request, 'symptoms/dashboard.html', {'questionnaires': questionnaires})
    
    if current_user.groups.filter(name="Health-Professional").exists():
        request.GET
        health_professional_profile_current_user = HealthProfessionalProfile.objects.get(user = current_user)
        patient_profiles = PatientProfile.objects.filter(health_professional = health_professional_profile_current_user)
        return render(request, 'symptoms/patients.html', {"patient_profiles":patient_profiles})

@login_required(login_url="/users/login")
def user_responses_view(request, slug):
    """View to display the responses of a single user."""
    requested_user_profile = get_object_or_404(PatientProfile, slug=slug)
    current_user = request.user
    questionnaires = Questionnaire.objects.all()

    if is_allowed_to_read(current_user, requested_user_profile):
        return render(request, 'symptoms/user_responses.html', {'requested_user_profile':requested_user_profile, 'questionnaires': questionnaires})
    else:
        return HttpResponseForbidden("You do not have permission to view this user's responses.")
    


@login_required(login_url="/users/login")
def get_questionnaire_scores(request, profile_slug):

    print("get_questionnaire_scores")
    """View to get the scores of a questionnaire for a specific user."""
    requested_user_profile = get_object_or_404(PatientProfile, slug=profile_slug)
    current_user = request.user
    questionnaire_id = request.GET.get("questionnaire_id")
    questionnaire = Questionnaire.objects.get(id = questionnaire_id)

    if is_allowed_to_read(current_user, requested_user_profile):
        responses = UserResponse.objects.filter(questionnaire = questionnaire, user = requested_user_profile.user)

        data = [response.get_score() for response in responses.all()]
        labels = [i for i in range(0, len(data))]

        return JsonResponse({'data': data, 'labels':labels})
    
    
    return JsonResponse({"error": "Invalid request"}, status=400)




"""choose questionnaire for symptom assessment"""
@login_required(login_url="/user/login")
def questionnaireSelection_view(request):

    questionnaires = Questionnaire.objects.all()

    return render(request, 'symptoms/questionnaireSelection.html', {"questionnaires": questionnaires})


@login_required(login_url="/users/login")
def symptomAssessment_view(request, questionnaire_id):

    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    questions = questionnaire.questions.all()
    form_list = [QuestionResponseForm(question) for question in questions]

    if request.method == "POST":
        form_list = [QuestionResponseForm(question, request.POST) for question in questions]

        if all(form.is_valid() for form in form_list):
            user_response = UserResponse.objects.create(questionnaire = questionnaire, user = request.user)
        
            for form in form_list:
                for question_id in form.cleaned_data:
                    q = Question.objects.get(id = int(question_id))
                    response = q.response_options.get(value = form.cleaned_data[question_id])
                    user_response.responses.add(response)

            UserResponse.save(user_response)

        messages.success(request, "Questionnaire submitted.")

        return redirect("symptoms:dashboard")
    
    return render(request, 'symptoms/symptomAssessment.html', {"form_list": form_list})