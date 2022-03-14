from django.shortcuts import render


# Create your views here.

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'user/sign_in.html')
