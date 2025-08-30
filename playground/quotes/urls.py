
from django.urls import path
# from .views import index
from . import views


urlpatterns = [
    # path('quotes/', index, name='index') # http://127.0.0.1:8000/quotes/
    # path('monday/', views.monday, name='monday'), # http://127.0.0.1:8000/quotes/monday/
    # path('tuesday/', views.tuesday, name='tuesday'), # http://127.0.0.1:8000/quotes/tuesday/
    path('<day>/', views.days_week, name='days_week'), # http://127.0.0.1:8000/quotes/<day>/
]
