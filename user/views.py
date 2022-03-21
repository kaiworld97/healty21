# 초기값
# from django.shortcuts import render


# # Create your views here.

# def sign_in(request):
#     if request.method == 'GET':
#         return render(request, 'user/sign_in.html')

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth

from user.models import UserModel

from django.contrib.auth.decorators import login_required

# Create your views here.

def signin(request):
    if request.method == "GET":
        return render(request, 'community/signin.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/community')
        else:
            return redirect('/')

def signup(request):
    if request.method == "GET":
        return render(request, 'community/signup.html')
        
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)

        if password != password2:
            return render(request, 'community/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'community/signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/signin')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')