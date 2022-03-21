import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from .models import User, UserProfile, UserFollowing


def home(request):
    user = request.user
    if user.is_authenticated :
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
            profile = form.save(commit=False)      # 저장 늦추기
            print(form.cleaned_data)
            profile.user = request.user
            profile.bmi = form.cleaned_data['weight'] / (form.cleaned_data['height']/100)**2
            profile.req_cal = 2000      # ! 나중에 변경

            profile.save()
            return redirect('home')     # ! 나중에 경쟁/game으로 변경
    else:
        form = ProfileForm()
    return render(request, 'user/profile.html', {'form': form})


@login_required()
def profile_update(request, pk):
    profile = get_object_or_404(UserProfile, user_id=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)      # 저장 늦추기
            profile.user = request.user
            profile.bmi = round(form.cleaned_data['weight'] / (form.cleaned_data['height']/100)**2, 2)
            profile.req_cal = 2000      # ! 나중에 변경
            profile.save()
            return redirect('home')     # ! 나중에 경쟁/game으로 변경
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'user/profile.html', {'form': form})


@login_required()
def follow(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)    # fllowing 할 사람
    following = UserFollowing.objects.filter(following_user=person, user=request.user)
    if person != request.user:
        if not following:
            UserFollowing.objects.create(following_user=person, user=request.user)
        else:
            following[0].delete()
    return redirect('home')


def people_list(request):  # TemplateView 고려
    return None