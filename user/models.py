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
    view_eval = models.BooleanField(default=False)
    # image = models.ImageField(upload_to=user_directory_path, default='default/healthy21.png')

    def get_absolute_url(self):
        return f"/users/{self.pk}/"


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    GENDER = [
        (None, '성별을 선택해주세요.'),
        ('M', '남성'),
        ('F', '여성')
    ]
    PUBLICPRIVATE = [('public', '공개'), ('private', '비공개')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_day = models.DateField()
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
    )
    bio = models.CharField(max_length=300, blank=True, help_text="간단한 소개 한마디.")
    bmi = models.FloatField()
    bmi_category = models.CharField(max_length=100, null=True)
    bmr = models.FloatField(null=True)
    age = models.IntegerField(null=True)
    public = models.CharField(
        max_length=20, blank=True, default='public',
        choices=PUBLICPRIVATE,
        help_text="챌린지 공개 여부를 선택해주세요."
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        default='default/healthy21.png',
        help_text="변경을 원하시면 업로드 해주세요. 자동으로 크롭됩니다.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Override the save method of the model
    def save(self):
        super().save()
        img = Image.open(self.image.path)  # Open image
        result_size = 300  # height, width

        # resize and crop image
        w, h = img.size
        if w > result_size or h > result_size:
            ratio = max(result_size / w, result_size / h)  # Resize based on on largest size (w, h)
            neww, newh = map(int, (w * ratio, h * ratio))
            output_size = (neww, newh)
            img.thumbnail(output_size)  # Resize image thumbnail((max w, max h))
        else:  # if image is smaller than expected size, then just crop
            result_size = min(w, h)
            neww, newh = w, h
        left = (neww - result_size) / 2
        top = (newh - result_size) / 2
        right = (neww + result_size) / 2
        bottom = (newh + result_size) / 2
        img = img.crop((left, top, right, bottom))  # Crop image center
        # img.show()
        img.save(self.image.path, quality=95)  # Save it again and override the larger image



class UserFollowing(models.Model):
    class Meta:
        db_table = "user_follow"

    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class UserBlocking(models.Model):
    class Meta:
        db_table = "user_block"

    user = models.ForeignKey(User, related_name="blocked", on_delete=models.CASCADE)
    blocking_user = models.ForeignKey(User, related_name="blocked_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
