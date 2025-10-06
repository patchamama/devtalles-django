
from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas de URL...
    path('', views.index, name='minilibrary'),  # Ruta para la vista de índice
]