from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),

    path('game', views.game, name='game'),
    path('set_goal', views.set_goal, name='set_goal'),
    # path('matching', views.matching, name='matching'),
    path('matching/<int:pk>',views.matching, name='matching'),
    path('game/<int:pk>',views.game_detail, name='game_detail'),
    path('game/followee/<int:pk>',views.compete_followee, name='compete_followee')



]