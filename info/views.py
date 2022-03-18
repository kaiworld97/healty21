from django.shortcuts import render, redirect
from .models import *

# Create your views here.


def info(request):
    if request.method == 'GET':
        return render(request, 'info/info.html')


def content_type(request, type):
    if request.method == 'GET':
        if type == 'diet_plan':
            return render(request, 'info/content_type.html', {'type': type})
        elif type == 'food':
            return render(request, 'info/content_type.html', {'type': type})
        elif type == 'workout':
            return render(request, 'info/content_type.html', {'type': type})
        elif type == 'workout_routine':
            return render(request, 'info/content_type.html', {'type': type})


def content_detail(request, pk):
    if request.method == 'GET':
        return render(request, 'info/content_detail.html')


def content_save(request, pk):
    if request.method == 'POST':
        return redirect(request.headers['Referer'])
