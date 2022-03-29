from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
import random


@login_required()
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
        page_number = request.GET.get('page')
        if not page_number:
            recommend = random.sample(list(Content.objects.filter(type=type)), 10)
            content = Content.objects.filter(type=type)[:30]
            return render(request, 'info/content_type.html', {'type': type, 'content': content, 'recommend': recommend})
        else:
            content_list = Content.objects.filter(type=type)
            paginator = Paginator(content_list, 10)

            if int(page_number) <= paginator.num_pages:
                obj_list = paginator.get_page(page_number)
                data_list = [{'id': obj.id, 'item': obj.item} for obj in obj_list]
                return JsonResponse(data_list, status=200, safe=False)


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