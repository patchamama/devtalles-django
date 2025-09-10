
from django.urls import path
from . import views


urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('detail/', views.course_detail, name='course_detail'),
    path('lesson/', views.course_lesson, name='course_lesson'),
]
