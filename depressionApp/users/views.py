from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register_view(request):
    # if user submits form, save the user to DB
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("symptoms:dashboard")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})