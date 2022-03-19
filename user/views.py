import os

from django.shortcuts import render, redirect
from .models import User, UserProfile, UserFollow, UserGroup
from .forms import ProfileForm


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'user/sign_in.html')


def home(request):
    print(request.user)
    return render(request, 'user/home.html')


def profile_create(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)      # 저장 늦추기
            profile.bmi = profile.weight / (profile.height/100)**2
            profile.req_cal = 2000      # ! 나중에 변경
            profile.save()
            return redirect('home')     # ! 나중에 경쟁/game으로 변경
    else:
        form = UserProfile()
        return render(request, 'user/user_profile.html', {'form': form})

