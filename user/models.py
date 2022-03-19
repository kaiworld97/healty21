from django.db import models
from django.contrib.auth.models import AbstractUser


class UserGroup(models.Model):
    class Meta:
        db_table = "user_group"

    goal = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return f"Group Type:{self.type} & Level: {str(self.level)}"


class User(AbstractUser):
    class Meta:
        db_table = "user"

    # nickname = models.CharField(max_length=15, unique=True, blank=True, null=True)    # 대신 username으로
    # user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, limit_choices_to={'surveyed': True})

    def clean(self):
        if self.nickname == "":
            self.nickname = None


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateTimeField(auto_now=False, auto_now_add=False)
    height = models.FloatField()
    weight = models.FloatField()
    GENDER = [
        ('M', '남성'),
        ('F', '여성'),
        (None, '성별을 선택해주세요.')
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    bio = models.TextField(null=True)
    bmi = models.IntegerField()
    req_cal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserFollow(models.Model):
    class Meta:
        db_table = "user_follow"

    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)