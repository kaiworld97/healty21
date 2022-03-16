from django.db import models
from user.models import UserModel
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Content(models.Model):
    class Meta:
        db_table = 'content'

    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    item = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    description = models.TextField(default='')


class VisitContent(models.Model):
    class Meta:
        db_table = 'visit_content'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    visit_count = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])


class SaveContent(models.Model):
    class Meta:
        db_table = 'save_content'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)


class Food(models.Model):
    class Meta:
        db_table = 'food'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, null=True)
    calories = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)


class DietPlan(models.Model):
    class Meta:
        db_table = 'diet_plan'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    food_list = models.ManyToManyField(Food, related_name='food_list', db_table='plan_food_list')
    meal_type = models.CharField(max_length=30)
    total_calories = models.IntegerField(null=True)


class Workout(models.Model):
    class Meta:
        db_table = 'workout'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    consume_cal = models.IntegerField(null=True)


class WorkoutRoutine(models.Model):
    class Meta:
        db_table = 'workout_routine'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    workout_list = models.ManyToManyField(Workout, related_name='workout_list', db_table='routine_workout_list')
    total_consume_cal = models.IntegerField(null=True)


class WorkoutCaloriesCalculate(models.Model):
    class Meta:
        db_table = 'workout_calories_calculate'

    workout = models.CharField(max_length=30)
    met = models.IntegerField()
