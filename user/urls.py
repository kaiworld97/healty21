from django.conf.urls.static import static
from django.urls import include, path

from config import settings

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("index/", views.index, name="index"),
    path(
        "profile/",
        include(
            [
                path("", views.profile, name="profile"),
                path("view/", views.profile_view, name="profile_view"),
                path("search/", views.profile_search, name="profile_search"),
            ]
        ),
    ),
    path("people/", views.people_list, name="people_list"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("<int:user_pk>/block/", views.block, name="block"),
]
