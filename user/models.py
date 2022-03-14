from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = "my_user"

    nick_name = models.CharField(max_length=15, unique=True, null=True)

    # def __str__(self):
    #     return self.email
