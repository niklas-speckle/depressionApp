from django.urls import path
from . import views

app_name = 'symptoms'

urlpatterns = [
    path('', views.dashboard, name = "dashboard"),
    path('symptomAssessment/', views.symptomAssessment_view, name="symptomAssessment")
]