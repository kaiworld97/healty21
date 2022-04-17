from django.db import models
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Content(models.Model):
    class Meta:
        db_table = 'content'

    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='content')
    item = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    description = models.TextField(default='')


class VisitContent(models.Model):
    class Meta:
        db_table = 'visit_content'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visit_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='visit_content')
    visit_count = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])


class SaveContent(models.Model):
    class Meta:
        db_table = 'save_content'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='save_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='save_content')


class Food(models.Model):
    class Meta:
        db_table = 'food'

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='food')
    category = models.CharField(max_length=30, null=True)
    calories = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    sodium = models.FloatField(null=True)
    maker = models.CharField(max_length=30, null=True)


class DietPlan(models.Model):
    class Meta:
        db_table = 'diet_plan'

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='diet_plan')
    food_list = models.ManyToManyField(Food, related_name='food_list', db_table='plan_food_list')
    meal_type = models.CharField(max_length=30)
    total_calories = models.FloatField(null=True)


class Workout(models.Model):
    class Meta:
        db_table = 'workout'

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='workout')
    body_part = models.CharField(max_length=30)
    kor_body_part = models.CharField(max_length=30)
    equipment = models.CharField(max_length=30)
    kor_equipment = models.CharField(max_length=30)
    gif_url = models.URLField()
    eng_name = models.CharField(max_length=30)
    target = models.CharField(max_length=30)
    kor_target = models.CharField(max_length=30)


class WorkoutRoutine(models.Model):
    class Meta:
        db_table = 'workout_routine'

    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='workout_routine')
    workout_list = models.ManyToManyField(Workout, related_name='workout_list', db_table='routine_workout_list')
    total_consume_cal = models.FloatField(null=True)


class WorkoutCaloriesCalculate(models.Model):
    class Meta:
        db_table = 'workout_calories_calculate'

    workout = models.CharField(max_length=30)
    met = models.FloatField()
