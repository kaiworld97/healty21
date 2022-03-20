from django.shortcuts import render, redirect
from .models import *
import random
# Create your views here.


def info(request):
    if request.method == 'GET':
        data = {}
        recommend = random.sample(list(Content.objects.all()), 10)
        food = random.sample(list(Content.objects.filter(type='food')), 10)
        # diet_plan = random.sample(list(Content.objects.filter(type='diet_plan')), 10)
        workout = random.sample(list(Content.objects.filter(type='workout')), 10)
        # workout_routine = random.sample(list(Content.objects.filter(type='workout_routine')), 10)
        data['recommend'] = recommend
        data['food'] = food
        # data['diet_plan'] = diet_plan
        data['workout'] = workout
        # data['workout_routine'] = workout_routine
        return render(request, 'info/info.html', {'data': data})


def content_type(request, type):
    if request.method == 'GET':
        if type == 'food':
            recommend = random.sample(list(Content.objects.filter(type='food')), 10)
            content = Content.objects.filter(type='food')[:10]
        elif type == 'diet_plan':
            recommend = random.sample(list(Content.objects.filter(type='diet_plan')), 10)
            content = Content.objects.filter(type='diet_plan')[:10]
        elif type == 'workout':
            recommend = random.sample(list(Content.objects.filter(type='workout')), 10)
            content = Content.objects.filter(type='workout')[:10]
        elif type == 'workout_routine':
            recommend = random.sample(list(Content.objects.filter(type='workout_routine')), 10)
            content = Content.objects.filter(type='workout_routine')[:10]
        return render(request, 'info/content_type.html', {'type': type, 'content': content, 'recommend': recommend})


def content_detail(request, pk):
    if request.method == 'GET':
        content = Content.objects.get(id=pk)
        type = content.type
        if type == 'food':
            data = Food.objects.get(content=content)
        elif type == 'diet_plan':
            data = DietPlan.objects.get(content=content)
        elif type == 'workout':
            data = Workout.objects.get(content=content)
        elif type == 'workout_routine':
            data = WorkoutRoutine.objects.get(content=content)
        return render(request, 'info/content_detail.html', {'type': type, 'data': data})


def content_save(request, pk):
    if request.method == 'POST':
        return redirect(request.headers['Referer'])
