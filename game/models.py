from django.db import models
from user.models import *


class Game(models.Model):
    class Meta:
        db_table = 'game'

    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, related_name='game')
    title = models.CharField(max_length=30)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    day = models.IntegerField(default=0)
    status = models.BooleanField(default=False)


class Competition(models.Model):
    class Meta:
        db_table = 'competition'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='competition')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competition')
    created_at = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(default=0)


class Competitor(models.Model):
    class Meta:
        db_table = 'competitor'

    competitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitor')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='competitor')


def quest_directory_path(instance, filename):
    return f'user_{instance.user.id}/quest/{filename}'


class Quest(models.Model):
    class Meta:
        db_table = 'quest'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='quest')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quest')
    type = models.CharField(max_length=30)
    point = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to=quest_directory_path, null=True, default='default/healthy21.png')
    content = models.TextField()
