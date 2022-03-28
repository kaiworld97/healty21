from django.shortcuts import render,redirect
from django.contrib import auth
from user.models import UserModel
from django.contrib.auth.decorators import login_required

# Create your views here.

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'user/sign_in.html')

def signup(request):
    if request.method == 'POST':
        # form 태그 요청일 때
        # 로그인
        # 아이디 중복 예외처리
        found_user = UserModel.objects.filter(username=request.POST['username'])
        if len(found_user) > 0:
            return render(request, 'user/signup.html',{'error':'username이 이미 존재합니다.'})
        else:
            new_user = UserModel.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                nick_name=request.POST['nickname']
            )
            auth.login(request, new_user)
            return redirect('index')

    else:

        return render(request, 'user/signup.html')

def signin(request):
    if request.method =='POST':
        #로그인
        found_user = auth.authenticate(request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if found_user is not None:
            auth.login(request, found_user)
            return redirect('index')
        else:
            return render(request, 'user/signin.html', {'error':'유저가 존재하지 않습니다.'})
    else:
        return render(request, 'user/signin.html')

@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('index')