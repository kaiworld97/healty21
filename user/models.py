from django.db import models
from django.contrib.auth.models import AbstractUser


class UserGroup(models.Model):
    class Meta:
        db_table = "user_group"

    type = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return self.type + str(self.level)


class User(AbstractUser):
    class Meta:
        db_table = "my_user"

    nickname = models.CharField(max_length=15, unique=True, blank=True, null=True)
    # user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, limit_choices_to={'surveyed': True})

    def clean(self):
        if self.nickname == "":
            self.nickname = None

    # def __str__(self):
    #     return self.email


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_day = models.DateTimeField(auto_now=False, auto_now_add=False)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    req_cal = models.IntegerField()
    bio = models.TextField(null=True)
