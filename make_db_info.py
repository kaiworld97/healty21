import os
import django
import csv
import sys

# 프로젝트 이름.settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from info.models import *  # django.setup() 이후에 임포트해야 오류가 나지 않음

with open('exercises_met.csv', encoding='UTF8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:
        cal = WorkoutCaloriesCalculate()
        cal.workout = row[0]
        cal.met = row[2]
        cal.save()


with open('food.csv', encoding='UTF8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)  # 출력시 함께 출력되는 맨첫줄을 제외하고 출력하기 위함
    for row in data_reader:
        cal = WorkoutCaloriesCalculate()
        cal.workout = row[0]
        cal.met = row[2]
        cal.save()