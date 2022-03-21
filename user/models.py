from django.db import models
from django.contrib.auth.models import AbstractUser


class UserGroup(models.Model):
    class Meta:
        db_table = "user_group"

    goal = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return f"그룹 타입: {self.goal} & 레벨: {str(self.level)}"


class User(AbstractUser):
    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    GENDER = [
        (None, '성별을 선택해주세요.'),
        ('M', '남성'),
        ('F', '여성')
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    bio = models.CharField(max_length=256, blank=True, help_text="간단한 소개 한마디")
    bmi = models.FloatField()
    bmi_category = models.CharField(max_length=256, null=True)
    req_cal = models.IntegerField()
    bmr = models.FloatField(null=True)
    age = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, limit_choices_to={'surveyed': True})

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserFollowing(models.Model):
    class Meta:
        db_table = "user_follow"

    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)