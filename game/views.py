from django.shortcuts import render, redirect
from user.models import User


# Create your views here.
def competition(request):
    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        if not user.group:
            return render(request, 'game/select.html', {'type': 'group'})
        elif not user.competition_activate:
            return render(request, 'game/select.html', {'type': 'competitor'})
        else:
            return render(request, 'game/competition.html')
    if request.method == 'POST':
        return redirect('/competition')
