from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserGroup(models.Model):
    class Meta:
        db_table = "user_group"

    goal = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return f"그룹 {self.goal} 레벨 {str(self.level)}"


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/profile/{filename}'


class User(AbstractUser):
    class Meta:
        db_table = "user"

    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    competition_activate = models.BooleanField(default=False)
    point = models.IntegerField(default=0)
    image = models.ImageField(upload_to=user_directory_path, default='default/healthy21.png')

    def get_absolute_url(self):
        return f"/users/{self.pk}/"

    # Override the save method of the model
    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)  # Open image
    #
    #     # resize image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)  # Resize image
    #         img.save(self.image.path)  # Save it again and override the larger image

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


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
    bio = models.CharField(max_length=300, blank=True, help_text="간단한 소개 한마디")
    bmi = models.FloatField()
    bmi_category = models.CharField(max_length=100, null=True)
    bmr = models.FloatField(null=True)
    age = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class UserFollowing(models.Model):
    class Meta:
        db_table = "user_follow"

    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


