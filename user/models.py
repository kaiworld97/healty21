# 초기값
# from django.db import models
# from django.contrib.auth.models import AbstractUser


# # Create your models here.

# class UserModel(AbstractUser):
#     class Meta:
#         db_table = "my_user"

#     nick_name = models.CharField(max_length=30)

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.URLField(max_length=200)
