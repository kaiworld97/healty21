from django.shortcuts import render, redirect
from django.http import HttpResponse

def community(request):
    return render(request, 'community/community.html')