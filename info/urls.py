from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info, name='info'),
    path('info/<str:type>/', views.content_type, name='content_type'),
    path('info/<int:pk>', views.content_detail, name='content_detail'),
    path('info/save/<int:pk>', views.content_save, name='content_save')
]
