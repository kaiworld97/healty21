import os
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from .models import User, UserProfile, UserFollowing


def home(request):
    user = request.user
    if user.is_authenticated:
        followings_list = UserFollowing.objects.filter(user=user).order_by('created_at')
        followings = [following.following_user for following in followings_list]

        nofollowings = [x for x in User.objects.all().exclude(id=user.id) if x not in followings]

        return render(request, 'user/home.html', {'followings': followings, 'nofollowings': nofollowings})
    else:
        return render(request, 'user/home.html')


@login_required()
def profile_create(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)  # 저장 늦추기
            profile.user = request.user
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height'] / 100
            # bmi 계산
            bmi = round(weight / (height * height), 1)
            # bmi 카테고리
            profile.bmi = bmi
            if bmi <= 18.5:
                bmi_category = '저체중 Underweight'
            elif bmi <= 24.9:
                bmi_category = '정상체중 Normal'
            elif bmi <= 29.9:
                bmi_category = '과체중 Overweight'
            else:
                bmi_category = '비만 Obesity'
            profile.bmi_category = bmi_category
            # 나이 계산
            today = date.today()
            born = form.cleaned_data['birth_day']
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            profile.age = age
            # 기초 대사량 계산
            if profile.gender == 'M':
                profile.bmr = round(66.4730 + (13.7516 * weight) + (5.0033 * height) - (6.7550 * age), 1)
            elif profile.gender == 'F':
                profile.bmr = round(655.0955 + (9.5634 * weight) + (1.8496 * height) - (4.6756 * age), 1)
            profile.save()
            return redirect('home')  # ! 나중에 경쟁/game으로 변경
    else:
        form = ProfileForm()
    return render(request, 'user/profile.html', {'form': form})


@login_required()
def profile_update(request, pk):
    profile = get_object_or_404(UserProfile, user_id=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)  # 저장 늦추기
            profile.user = request.user
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height'] / 100
            # bmi 계산
            bmi = round(weight / (height * height), 1)
            # bmi 카테고리
            profile.bmi = bmi
            if bmi <= 18.5:
                bmi_category = '저체중 Underweight'
            elif bmi <= 24.9:
                bmi_category = '정상체중 Normal'
            elif bmi <= 29.9:
                bmi_category = '과체중 Overweight'
            else:
                bmi_category = '비만 Obesity'
            profile.bmi_category = bmi_category
            # 나이 계산
            today = date.today()
            born = form.cleaned_data['birth_day']
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            profile.age = age
            # 기초 대사량 계산
            if profile.gender == 'M':
                profile.bmr = round(66.4730 + (13.7516 * weight) + (5.0033 * height) - (6.7550 * age), 1)
            elif profile.gender == 'F':
                profile.bmr = round(655.0955 + (9.5634 * weight) + (1.8496 * height) - (4.6756 * age), 1)
            profile.save()
            return redirect('home')  # ! 나중에 경쟁/game으로 변경
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'user/profile.html', {'form': form})


@login_required()
def follow(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)  # fllowing 할 사람
    following = UserFollowing.objects.filter(following_user=person, user=request.user)
    if person != request.user:
        if not following:
            UserFollowing.objects.create(following_user=person, user=request.user)
        else:
            following[0].delete()
    return redirect('home')


def people_list(request):  # TemplateView 고려
    return None
