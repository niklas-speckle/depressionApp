
from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Question, UserResponse
from .view_models.questionnaire import QuestionResponseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from users.models import HealthProfessionalProfile, PatientProfile

# Create your views here.

@login_required(login_url="/users/login")
def dashboard(request):

    current_user = request.user

    if current_user.groups.filter(name="Patient").exists():
        questionnaires = Questionnaire.objects.all()
        return render(request, 'symptoms/dashboard.html', {'questionnaires': questionnaires})
    
    elif current_user.groups.filter(name="Health-Professional").exists():
        health_professional_profile_current_user = HealthProfessionalProfile.objects.get(user = current_user)
        patients = PatientProfile.objects.filter(health_professional = health_professional_profile_current_user)

        print(patients)

        return render(request, 'symptoms/patients.html', {"patients":patients})


@login_required(login_url="/users/login")
def get_questionnaire_scores(request):

    if request.method == "GET":
        questionnaire_id = request.GET.get("questionnaire_id")

        current_user = request.user
        questionnaire = Questionnaire.objects.get(id = questionnaire_id)

        if questionnaire:

            responses = UserResponse.objects.filter(questionnaire = questionnaire, user = current_user)

            data = [response.get_score() for response in responses.all()]
            #labels = [response.date.strftime("%d/%m") for response in responses.all()]
            labels = [i for i in range(0, len(data))]

            print("Sent data:")
            print(data)
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