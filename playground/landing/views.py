from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'landing/landing.html', {
        "name": "Mandy",
        "age": 30
    })