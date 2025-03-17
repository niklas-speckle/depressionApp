from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Question, UserResponse
from .view_models.questionnaire import QuestionResponseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required(login_url="/users/login")
def dashboard(request):
    current_user = request.user
    assessments = UserResponse.objects.filter(user = current_user)
    return render(request, 'symptoms/dashboard.html', {'assessments': assessments})


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