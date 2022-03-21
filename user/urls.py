# 초기값
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('sign_in/', views.sign_in, name='sign_in'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout, name="logout"),
]