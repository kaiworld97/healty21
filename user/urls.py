from django.conf.urls.static import static
from django.urls import path, include

from config import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/<int:pk>/edit/', views.profile_update, name='profile_update'),
    path('people/', views.people_list, name='people_list'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)