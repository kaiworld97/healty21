from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile-create/', views.profile_create, name='profile-create')
]
