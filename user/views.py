from django.shortcuts import render


# Create your views here.

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'user/sign_in.html')


def home(request):
    print(request.user)
    return render(request, 'user/home.html')
