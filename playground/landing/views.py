from django.shortcuts import render
from datetime import date


# Create your views here.
def home(request):
    stack = ['Python', 'Django', 'JavaScript', 'React']
    
    return render(request, 'landing/landing.html', {
        "name": "Mandy",
        "age": 30,
        "current_date": date.today(),
        "stack": stack
    })