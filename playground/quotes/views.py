from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("¡Hola mundo desde django!")

# def monday(request):
#     return HttpResponse("¡Hola Monday!")

# def tuesday(request):
#     return HttpResponse("¡Hola Tuesday!")

def days_week(request, day):
    # return HttpResponse(f"¡Hola {day}!")
    quote_text = None
    if day == "monday":
        quote_text = "El éxito es la suma de pequeños esfuerzos repetidos día tras día."
    elif day == "tuesday":
        quote_text = "La única forma de hacer un gran trabajo es amar lo que haces."
    elif day == "wednesday":
        quote_text = "No cuentes los días, haz que los días cuenten."
    elif day == "thursday":     
        quote_text = "El futuro pertenece a quienes creen en la belleza de sus sueños."
    elif day == "friday":
        quote_text = "La vida es 10% lo que me ocurre y 90% cómo reacciono a ello."
    elif day == "saturday":
        quote_text = "No esperes. El tiempo nunca será justo."
    elif day == "sunday":
        quote_text = "La mejor manera de predecir el futuro es crearlo."
    else:
        quote_text = "Día no válido. Por favor, elige un día de la semana."
    return HttpResponse(quote_text)