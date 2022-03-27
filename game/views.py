from django.shortcuts import render, redirect
from user.models import User, UserGroup
from .models import *
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.messages import error


def competition(request):
    user = User.objects.get(username=request.user)
    if request.method == 'GET':
        # 그룹이 없다면 그룹 설정
        if not user.group:
            groups = UserGroup.objects.all()
            return render(request, 'game/select.html', {'type': 'group', 'groups': groups})
        # 경쟁 상태가 아니라면 경쟁자 선정 후 경쟁 생성
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
            return render(request, 'game/competition.html',
                          {'competition': competition, 'competitors': competitors, 'quests': quests,
                           'nominated': nominated})
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
    if request.method == 'GET':
        # 날짜별 퀘스트 가져오기
        username = request.GET.get('username')
        user_quest = User.objects.get(username=username)
        # 처음 퀘스트 로그로 들어올 때
        if not request.GET.get('date'):
            start_date = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            end_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            quests = user_quest.quest.filter(upload_date__range=[start_date, end_date]).order_by('-upload_date')
            game_date = user.group.game.last()
            game_start = game_date.start_date
            game_end = game_date.end_date
            return render(request, 'game/quest.html', {'quests': quests, 'username': username, 'game_start': game_start, 'game_end': game_end})
        # 날짜를 선택할 때
        else:
            start_date = request.GET.get('date')
            end_date = (datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d') + datetime.timedelta(
                days=1)).strftime("%Y-%m-%d")
            quests = user_quest.quest.filter(upload_date__range=[start_date, end_date]).order_by('-upload_date')
            quest_list = []
            for quest in quests:
                q = {}
                q['upload_date'] = quest.upload_date.strftime("%Y년 %m월 %d일 %H시 %M분")
                q['photo'] = quest.photo.url
                q['content'] = quest.content
                q['username'] = quest.user.username
                quest_list.append(q)
            return JsonResponse(quest_list, status=200, safe=False)
    if request.method == 'POST':
        start_date = datetime.datetime.today().strftime("%Y-%m-%d")
        end_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        user_quest = Quest.objects.filter(user=user, upload_date__range=[start_date, end_date])
        # 오늘 퀘스트 4개 했으면 return
        if len(user_quest) == 4:
            error(request, '일일 퀘스트 4회를 완료했습니다.')
            return redirect('/competition')
        quest = Quest()
        quest.user = user
        quest.game = user.group.game.last()
        quest.type = request.POST['type']
        quest.point = 5
        quest.content = request.POST['content']
        try:
            quest.photo = request.FILES['input_file']
        except:
            pass
        quest.save()
        user.point += 5
        user.save()
        competition = user.competition.last()
        competition.point += 5
        competition.save()
        return redirect('/competition')
