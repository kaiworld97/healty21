from django.db import models
from user.models import UserModel
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class ContentModel(models.Model):
    class Meta:
        db_table = 'content'

    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    item = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    description = models.TextField()


class VisitContentModel(models.Model):
    class Meta:
        db_table = 'visit_content'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    visit_count = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
            ])


class SaveContentModel(models.Model):
    class Meta:
        db_table = 'save_content'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)


class FoodModel(models.Model):
    class Meta:
        db_table = 'food'

    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, null=True)
    calories = models.IntegerField(null=True)
    protein = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)


class DietPlanModel(models.Model):
    class Meta:
        db_table = 'diet_plan'

    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    food_list = models.ManyToManyField(FoodModel, related_name='food_list', db_table='plan_food_list')
    meal_type = models.CharField(max_length=30)
    total_calories = models.IntegerField()


class WorkoutModel(models.Model):
    class Meta:
        db_table = 'workout'

    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    consume_cal = models.IntegerField(null=True)
    description = models.TextField()


class WorkoutRoutineModel(models.Model):
    class Meta:
        db_table = 'workout_routine'

    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    workout_list = models.ManyToManyField(WorkoutModel, related_name='workout_list', db_table='routine_workout_list')
    total_consume_cal = models.IntegerField()
