import os
import django
import csv
import sys

# 프로젝트 이름.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from info.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음
User.objects.get_or_create(username='admin', password=1111, email='admin@admin.admin')
admin = User.objects.get(username='admin')
print('exercises_met.csv를 db에 추가합니다')
with open('info_db_csv/exercises_met.csv') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:
        cal = WorkoutCaloriesCalculate()
        cal.workout = row[0]
        cal.met = float(row[2])
        cal.save()
print('exercises.csv를 db에 추가합니다')
with open('info_db_csv/exercises.csv', encoding='UTF8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:
        content = Content()
        content.author = admin
        content.item = row[7]
        content.type = 'workout'
        content.description = row[6]
        content.save()
        workout = Workout()
        workout.content = content
        workout.body_part = row[0]
        workout.kor_body_part = row[1]
        workout.equipment = row[2]
        workout.kor_equipment = row[3]
        workout.gif_url = row[4]
        workout.eng_name = row[6]
        workout.target = row[8]
        workout.kor_target = row[9]
        workout.save()

food_list = ['다이어트 식품', '과자', '간편 식품', '프랜차이즈 음료', '프랜차이즈 식품', '제빵 식품', '기능성 음료']

for i in range(7):
    print(f'food{i}.csv를 db에 추가합니다')
    with open(f'info_db_csv/food{i}.csv', encoding='UTF8') as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            content = Content()
            content.author = admin
            content.item = row[0]
            content.type = 'food'
            content.description = row[0]
            content.save()
            food = Food()
            food.content = content
            food.maker = row[2]
            food.category = food_list[i]
            food.calories = float(row[6])
            food.protein = float(row[11])
            food.carbs = float(row[8])
            food.fat = float(row[10])
            food.sodium = float(row[7])
            food.save()

print('k_food.csv를 db에 추가합니다')
with open('info_db_csv/k_food.csv') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        content = Content()
        content.author = admin
        content.item = row[0]
        content.type = 'food'
        content.description = row[0]
        content.save()
        food = Food()
        food.content = content
        food.category = '한식'
        food.calories = float(row[1])
        food.protein = float(row[3])
        food.carbs = float(row[2])
        food.fat = float(row[4])
        food.sodium = float(row[7])
        food.save()

print('info db 완료')