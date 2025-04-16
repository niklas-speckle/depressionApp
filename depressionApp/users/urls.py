from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name = "register"),
    path('login/', views.login_view, name = "login"),
    path('logout/', views.logout_view, name = "logout"),
    path('create-therapy-agreement/', views.create_therapy_agreement, name = "create_therapy_agreement"),
]