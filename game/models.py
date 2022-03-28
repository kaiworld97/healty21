from django.db import models
from user.models import UserModel
# Create your models here.


class UserHealthInfo(models.Model):
    class Meta:
        db_table = "health_info"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    #User 가 사라진다며, 유저가 작성한 데이터도 같이 삭제해달라는 옵션
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    bmi = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Group(models.Model):
    class Meta:
        db_table = "group_info"

    type = models.CharField(max_length=256)
    level =models.IntegerField(default=0)

class Game(models.Model):
    class Meta:
        db_table = "game_info"

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length = 256)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=False)
    status = models.BooleanField(default=False)

class Competition(models.Model):
    class Meta:
        db_table = "Competition"
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)

class Competitor(models.Model):
    class Meta:
        db_table = "Competitor"
    competitor_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE,related_name='com')

class Quest(models.Model):
    class Meta:
        db_table = "Quest"

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=256)
    point = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(blank=True)
    content = models.TextField()
