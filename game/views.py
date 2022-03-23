from django.shortcuts import render, redirect
from user.models import User, UserGroup
from .models import *
import datetime
from django.db.models import Q


def competition(request):
    user = User.objects.get(username=request.user)
    if request.method == 'GET':
        if not user.group:
            groups = UserGroup.objects.all()
            return render(request, 'game/select.html', {'type': 'group', 'groups': groups})
        elif not user.competition_activate:
            # 유저 추천이 들어갈 부분
            competitors = User.objects.exclude(username=request.user)
            return render(request, 'game/select.html', {'type': 'competitor', 'competitors': competitors})
        else:
            # 현재 진행중인 competition 가져오기
            competition = user.competition.last()
            # 현재 competition에서 모든 경쟁자 가져오기
            competitors = competition.competitor.all()
            # competition 에 속한 competitor의 quest 가져오기
            q = Q()
            q.add(Q(user=user), q.OR)
            for competitor in competitors:
                q.add(Q(user=competitor.competitor), q.OR)
            quests = user.competition.last().game.quest.filter(q).order_by('-upload_date')
            # 유저가 속해져 있는 모든 경쟁 상대 보기
            nominated = user.competitor.all()
            return render(request, 'game/competition.html', {'competition': competition, 'competitors': competitors, 'quests': quests, 'nominated': nominated})
    if request.method == 'POST':
        if 'group' in request.POST:
            user.group = UserGroup.objects.get(id=request.POST['group'])
            user.save()
        elif 'competitor' in request.POST:
            game = user.group.game.last()
            competition = Competition.objects.create(game=game, user=user)
            # 선택한 competitor들 저장
            for competitor_email in request.POST.getlist('competitor'):
                competitor = Competitor()
                competitor.competition = competition
                competitor.competitor = User.objects.get(email=competitor_email)
                competitor.save()
            user.competition_activate = True
            user.save()
        return redirect('/competition')


def quest(request):
    user = User.objects.get(username=request.user)
    start_date = "2022-03-22"
    end_date = "2022-03-23"
    if request.method == 'GET':
        username = request.GET.get('username')
        user_quest = User.objects.get(username=username)
        quests = user_quest.quest.all().order_by('-upload_date')
        return render(request, 'game/quest.html', {'quests': quests})
    if request.method == 'POST':
        print(request.FILES)
        # print(request.FILES['input_file'])
        print(request.POST['type'])
        print(request.POST['content'])
        quest = Quest()
        quest.user = user
        quest.game = user.group.game.last()
        quest.type = request.POST['type']
        quest.point = 5
        quest.content = request.POST['content']
        # if request.FILES['input_file']:
        #     quest.photo = request.FILES['input_file']
        quest.save()
        return redirect('/competition')