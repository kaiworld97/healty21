from django.urls import path
from . import views

urlpatterns = [
    path('community/', views.community, name="community"),
    path('post/', views.post, name="post"),
    path('community/delete/<int:id>', views.post_delete, name="post_delete"),
    path('community/<int:id>', views.post_detail, name="post_detail"),
    path('community/comment/<int:id>', views.write_comment, name="write_comment"),
    path('community/comment/delete/<int:id>', views.delete_comment, name="delete_comment"),
    path('like/<int:post_id>', views.like, name="likes"),
]