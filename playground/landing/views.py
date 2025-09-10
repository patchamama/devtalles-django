from django.http import HttpResponse
from django.shortcuts import render
from datetime import date


# Create your views here.
def home(request):
    # stack = ['Python', 'Django', 'JavaScript', 'React']
    stack = [
        {'id': "python", 'name': 'Python', 'proficiency': 'Advanced'},
        {'id': "django", 'name': 'Django', 'proficiency': 'Intermediate'},
        {'id': "javascript", 'name': 'JavaScript', 'proficiency': 'Intermediate'},]

    return render(request, 'landing/landing.html', {
        "name": "Mandy",
        "age": 30,
        "current_date": date.today(),
        "stack": stack
    })
    
def stack_detail(request, tool):
    return HttpResponse(f"Detail of tool: {tool}")
    # return render(request, 'landing/stack_detail.html', {
    #     "tool": tool
    # })