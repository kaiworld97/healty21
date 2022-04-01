from django.conf.urls.static import static
from django.urls import include, path

from config import settings

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "profile/",
        include(
            [
                path("", views.profile, name="profile"),
                # path('<int:pk>/edit/', views.profile_update, name='profile_update'),
                path("<int:pk>/", views.profile_view, name="profile_view"),
            ]
        ),
    ),
    path("people/", views.people_list, name="people_list"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("<int:user_pk>/block/", views.block, name="block"),
]
