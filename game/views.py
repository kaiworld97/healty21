from django.shortcuts import render, redirect
from user.models import User, UserGroup
from .models import *
import datetime


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
            competition = user.competition.all().last()
            # 몇일 진행중 계산
            # days = str(datetime.datetime.now() - datetime.datetime.fromtimestamp(competition.game.start_date.timestamp()))
            # if 'days,' in days.split(' '):
            #     day = days.split(' ')[0] + '일 진행중'
            # else:
            #     day = '0일 진행중'
            # print(day)
            # 현재 competition에서 모든 경쟁자 가져오기
            competitors = competition.competitor.all()
            # competition 에 속한 competitor의 quest 가져오기
            # for competitor in competitors:
            #     competitor.competition.game.quest.all()
            # 유저가 속해져 있는 모든 경쟁 상대 보기
            # for i in user.competitor.all():
            #     print(i.competition.user)
            return render(request, 'game/competition.html', {'competition': competition, 'competitor': competitors})
    if request.method == 'POST':
        if 'group' in request.POST:
            user.group = UserGroup.objects.get(id=request.POST['group'])
            user.save()
        elif 'competitor' in request.POST:
            game = Game()
            game.group = user.group
            game.title = f'{request.user}님의 경쟁'
            # 기준일이 없어서 일단 현재 시간부터 + 21일
            game.end_date = datetime.datetime.now() + datetime.timedelta(days=21)
            game.save()
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
    end_date = "2022-03-22"
    if request.method == 'GET':
        user.quest.filter(upload_date__range=[start_date, end_date])
        return render(request, 'game/quest.html')
    if request.method == 'POST':
        return redirect('/competition')