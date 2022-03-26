from django.conf.urls.static import static
from django.urls import path, include

from config import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('profile/create/', views.profile_create, name='profile_create'),
    # path('profile/<int:pk>/edit/', views.profile_update, name='profile_update'),
    # path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    path('profile/', include([
        path('', views.profile_view, name='profile_create'),
        path('<int:pk>/edit/', views.profile_update, name='profile_update'),
        path('<int:pk>/', views.profile_view, name='profile_view'),
    ])),
    path('people/', views.people_list, name='people_list'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]

