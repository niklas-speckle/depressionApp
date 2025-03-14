from django.shortcuts import render

# Create your views here.

def symptoms(request):
    return render(request, 'symptoms/symptoms_list.html')