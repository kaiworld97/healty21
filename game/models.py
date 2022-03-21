from django.db import models
from user.models import *


class Game(models.Model):
    class Meta:
        db_table = "game"

    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.BooleanField(default=False)


class Competition(models.Model):
    class Meta:
        db_table = "competition"

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)


class Competitor(models.Model):
    class Meta:
        db_table = "competitor"

    competitor = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)


class Quest(models.Model):
    class Meta:
        db_table = "quest"

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    point = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(null=True)
    content = models.TextField()
