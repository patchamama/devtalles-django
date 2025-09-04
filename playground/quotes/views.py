from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


days_of_week = {
    "monday": "Piensos en grande y no te detengas hasta que estés orgulloso.",
    "tuesday": "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito.",
    "wednesday": "La disciplina es el puente entre las metas y los logros.",
    "thursday": "No sueñes con el éxito, trabaja para conseguirlo.",
    "friday": "Cada día es una nueva oportunidad para cambiar tu vida.",
    "saturday": "La perseverancia es la clave del éxito.",
    "sunday": "El único lugar donde el éxito viene antes que el trabajo es en el diccionario."
}

def days_week(request, day):
    # return HttpResponse(f"¡Hola {day}!")
    # quote_text = None
    # day = day.lower()  # Convertir a minúsculas para hacer la comparación insensible a mayúsculas
    # if day in days_of_week:
    #     quote_text = days_of_week[day]
    # else:
    #     quote_text = "Día no válido. Por favor, elige un día de la semana."
    # return HttpResponse(quote_text)
    try:
        quote_text = days_of_week[day.lower()]  # Convertir a minúsculas para hacer la comparación insensible a mayúsculas
        return HttpResponse(quote_text)
    except KeyError:
        return HttpResponse("Día no válido. Por favor, elige un día de la semana.") 
    


def days_week_with_number(request, day):
    days = list(days_of_week.keys() )  # Obtener la lista de días de la semana
    if day > len(days) or day < 1:
        return HttpResponseNotFound("Número de día no válido. Por favor, elige un número entre 1 y 7.")
    redirect_day = days[day - 1]  # Obtener el nombre del día correspondiente al número
    return HttpResponseRedirect(f"/quotes/{redirect_day}/")  # Redirigir a la URL correcta

    # days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    # if 1 <= day <= 7:
    #     day_name = days[day - 1]
    #     return days_week(request, day_name)  # Llamar a la función days_week para obtener la cita
    #     # return HttpResponse(f"El día {day} corresponde a {day_name}.")
    # else:
    #     return HttpResponse("Número de día no válido. Por favor, elige un número entre 1 y 7.")