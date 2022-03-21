from django.urls import path
from . import views

urlpatterns = [
    path('competition/', views.competition, name='competition'),
]