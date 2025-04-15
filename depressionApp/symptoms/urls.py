from django.urls import path
from . import views

app_name = 'symptoms'

urlpatterns = [
    path('', views.dashboard, name = "dashboard"),
    path('symptomAssessment/<int:questionnaire_id>', views.symptomAssessment_view, name="symptomAssessment"),
    path('questionnaireSelection/', views.questionnaireSelection_view, name="questionnaireSelection"),
    path('patients/questionnaire_scores/<slug:profile_slug>/', views.get_questionnaire_scores, name="questionnaire_scores"),
    path('patients/', views.dashboard, name="patients"),
    path('patients/<slug:slug>/', views.user_responses_view, name="user_responses"),
]