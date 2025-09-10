from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # http://127.0.0.1:8000/home
    path('stack/<str:tool>/', views.stack_detail, name='stack'), # http://127.0.0.1:8000/stack/Python/
]