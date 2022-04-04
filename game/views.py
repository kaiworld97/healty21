from django.shortcuts import render, redirect
from user.models import User, UserGroup
from .models import *
import datetime
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required
import random


@login_required()
def competition(request):
    user = request.user
    if request.method == 'GET':
        # 그룹이 없다면 그룹 설정
        if not user.group:
            groups = UserGroup.objects.all()
            return render(request, 'game/select.html', {'type': 'group', 'groups': groups})
        # 경쟁 상태가 아니라면 경쟁자 선정 후 경쟁 생성
        elif not user.competition_activate:
            # 유저 추천이 들어갈 부분
            if user.point == 0 and (
                    len((users_by_points := User.objects.filter(group=user.group, point=0).exclude(id=user.id))) <= 5):
                users_by_points = User.objects.filter(group=user.group).exclude(id=user.id).order_by('point')[:5]
            elif user.point == 0:
                users_by_points = random.sample(list(users_by_points), 5)
            else:
                # 같은 그룹과 유사한 포인트 가진 사람 보여주기
                users_by_groups = User.objects.filter(group=user.group).exclude(id=user.id)  # 유저 그룹으로 1차 필터링
                # 유저와 포인트 차이로 sort하고 5명까지
                users_by_points = sorted(users_by_groups, key=lambda x: abs(x.point - user.point))[:5]
            return render(request, 'game/select.html', {'type': 'competitor', 'competitors': users_by_points})
        else:
            page_number = request.GET.get('page')
            # 현재 진행중인 competition 가져오기
            competition = user.competition.last()
            # 현재 competition에서 모든 경쟁자 가져오기
            competitors = competition.competitor.all()
            q = Q()
            # 경쟁 시작한 날부터 퀘스트 불러오기
            if (datetime.datetime.today() - competition.created_at).days < 7:
                start_date = competition.created_at.strftime("%Y-%m-%d")
                end_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                start_date = (datetime.datetime.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
                end_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            # competition 에 속한 competitor의 quest 가져오기
            q.add(Q(user=user), q.OR)
            for competitor in competitors:
                q.add(Q(user=competitor.competitor), q.OR)
            all_quests = competition.game.quest.filter(Q(upload_date__range=[start_date, end_date]) & q).order_by(
                '-upload_date')
            if not page_number:
                quests = all_quests[:10]
                # competitors의 점수
                point = [{'username': user.username, 'point': competition.point}]
                for competitor in competitors:
                    point.append({'username': competitor.competitor.username,
                                  'point': sum(map(lambda x: x.point,
                                                   filter(lambda
                                                              x: x.user.username == competitor.competitor.username,
                                                          all_quests)))})
                points = sorted(point, key=lambda x: -x['point'])
                # 유저가 속해져 있는 모든 경쟁 상대 보기
                nominated = user.competitor.all()
                return render(request, 'game/competition.html',
                              {'competition': competition, 'competitors': competitors, 'quests': quests,
                               'nominated': nominated, 'points': points})
            else:
                paginator = Paginator(all_quests, 10)
                if int(page_number) <= paginator.num_pages:
                    obj_list = paginator.get_page(page_number)
                    data_list = [{'username': obj.user.username, 'photo': obj.photo.url, 'content': obj.content,
                                  'date': obj.upload_date.strftime("%Y년 %m월 %d일 %H시 %M분")} for obj in obj_list]
                    return JsonResponse(data_list, status=200, safe=False)
                elif int(page_number) > paginator.num_pages:
                    return HttpResponse(status=404)

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


@login_required()
def quest(request):
    user = request.user
    if request.method == 'GET':
        # 날짜별 퀘스트 가져오기
        username = request.GET.get('username')
        user_quest = User.objects.get(username=username)
        # 처음 퀘스트 로그로 들어올 때
        if not request.GET.get('date'):
            start_date = datetime.datetime.today().strftime("%Y-%m-%d")
            end_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            quests = user_quest.quest.filter(upload_date__range=[start_date, end_date]).order_by('-upload_date')
            game_date = user.group.game.last()
            game_start = game_date.start_date
            game_end = game_date.end_date
            return render(request, 'game/quest.html',
                          {'quests': quests, 'username': username, 'game_start': game_start, 'game_end': game_end})
        # 날짜를 선택할 때
        else:
            start_date = request.GET.get('date')
            end_date = (datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d') + datetime.timedelta(
                days=1)).strftime("%Y-%m-%d")
            quests = user_quest.quest.filter(upload_date__range=[start_date, end_date]).order_by('-upload_date')
            if len(quests) == 0:
                return HttpResponse(status=404)
            quest_list = []
            for quest in quests:
                q = {}
                q['upload_date'] = quest.upload_date.strftime("%Y년 %m월 %d일 %H시 %M분")
                q['photo'] = quest.photo.url
                q['content'] = quest.content
                q['username'] = quest.user.username
                q['id'] = quest.id
                quest_list.append(q)
            return JsonResponse(quest_list, status=200, safe=False)

    if request.method == 'POST':
        start_date = datetime.datetime.today().strftime("%Y-%m-%d")
        end_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        user_quest = Quest.objects.filter(user=user, upload_date__range=[start_date, end_date]).order_by('-upload_date')
        # 오늘 퀘스트 4개 했으면 return
        if len(user_quest) == 4:
            error(request, '일일 퀘스트 4회를 완료했습니다.')
            return redirect('/competition')
        # 같은 타입의 퀘스트가 1시간 이내에 들어오면 return
        elif (len(user_quest) > 0 and user_quest[0].type == request.POST['type'] and (
                datetime.datetime.today() - user_quest[0].upload_date).seconds < 3600) or (
                len(user_quest) > 1 and user_quest[1].type == request.POST['type'] and (
                datetime.datetime.today() - user_quest[1].upload_date).seconds < 3600):
            error(request, '같은 타입의 퀘스트는 1시간이 지나야 합니다.')
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
