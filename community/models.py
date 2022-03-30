from django.db import models
from django import forms
from user.models import UserModel
from taggit.managers import TaggableManager


class Post(models.Model):
    class Meta:
        db_table = "community_post"
    
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField()
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(UserModel, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        db_table = "comment"
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    like = models.ManyToManyField(UserModel, related_name='comment_like', blank=True)
    like_count = models.PositiveIntegerField(default=0)