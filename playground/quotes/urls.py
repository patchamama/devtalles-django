
from django.urls import path
# from .views import index
from . import views


urlpatterns = [
    # path('quotes/', index, name='index') # http://127.0.0.1:8000/quotes/
    # path('monday/', views.monday, name='monday'), # http://127.0.0.1:8000/quotes/monday/
    # path('tuesday/', views.tuesday, name='tuesday'), # http://127.0.0.1:8000/quotes/tuesday/
    path('', views.index, name='index'), # http://127.0.0.1:8000/quotes/
    path('<int:day>/', views.days_week_with_number, name='days_week_with_number'), # http://127.0.0.1:8000/quotes/<day>/
    path('<str:day>/', views.days_week, name='days_quote'), # http://127.0.0.1:8000/quotes/<day>/
   
]
