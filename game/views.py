from django.shortcuts import render,redirect
from user.models import UserModel
from .models import Group,Game, Competition, Competitor, Quest
from django.contrib.auth.decorators import login_required
import datetime



# Create your views here.
def index(request):
    #임시로 만든 로그인 후 index 페이지

    #새로운 UserGroup이 추가되거나, 게임이 종료되면 자동으로 기간을 조회해 게임되는 로직. 임시로 구현해봄
    groups = Group.objects.all()
    for group in groups:
        game = Game.objects.filter(group_id=group)
        print(len(game))
        if len(game) < 1 :
            end_date = datetime.date.today() + datetime.timedelta(weeks=3)

            new_game = Game.objects.create(
                group_id = group,
                title = f'{group.type}의 게임',
                status = 'True',
                end_date= end_date,
            )
        if game.values('status') == 'False':
            end_date = datetime.date.today() + datetime.timedelta(weeks=3)
            renew_game = Game.objects.create(
                group_id=group,
                title=f'{group.type}의 게임',
                status='True',
                end_date=end_date,
            )
    return render(request, 'game/index.html')

def game(request):  # 경쟁시스템 관련 메인페이지
    username = request.user

    #내가 참여한 경쟁 목록
    my_competition = Competition.objects.filter(user_id=request.user)

    #경쟁목록의 경쟁상대
    my_competitor = Competitor.objects.filter(competition_id__in=my_competition)

    #나를 지목한 경쟁상대를 확인하기 위한 필터
    competitors_chooseme = Competitor.objects.filter(competitor_id=request.user).values('competition_id')
    competitions = Competition.objects.filter(pk__in=competitors_chooseme)


    return render(request, "game/competition.html",{'competitions':competitions,
                                                    'username':username,
                                                    'my_competitions':my_competition,
                                                    'my_competitor':my_competitor})

@login_required(login_url='signin')
def set_goal(request):  #사용자가 목표그룹 목록을 볼 수 있는 페이지
    groups = Group.objects.all()

    return render(request, "game/set_goal.html",{'groups':groups})

def matching(request,pk): #목표그룹에서 선택한 그룹으로 선택하는 페이지
    group = Group.objects.get(pk=pk)

    #(임시설정)선택하기를 누르면 유저 정보가 업데이트됨
    if request.method == 'POST':
        user=UserModel.objects.get(username=request.user)
        user.group_id= group
        user.save()

        return redirect('game')

    return render(request, "game/matching.html", {'group':group})

@login_required(login_url='signin')
def select_compete(request):    #같은 목표그룹의 유저를 경쟁상대로 선택할수 있는 페이지
    group = request.user.group_id
    members = UserModel.objects.filter(group_id=group)
    game = Game.objects.get(group_id=group)

    #(임시설정) 지목할 유저의 닉네임을 input에 입력하면 그 사람과 매칭되는 로직
    if request.method == 'POST':
        chosen_competitor = request.POST['nick_name']
        competition = Competition.objects.create(
            game_id= game,
            user_id= request.user,

        )
        competitor = Competitor.objects.create(
            competitor_id=UserModel.objects.get(nick_name=chosen_competitor),
            competition_id=competition
        )
        return redirect('game')
    return render(request, "game/select_compete.html",{'group':group,'members':members})

def game_detail(request,pk): #경쟁에 대한 상세보기 페이지
    #competition을 pk로 받아온 페이지
    competition = Competition.objects.get(pk=pk)

    #user_id로 Quest에서 필터
    my_quest = Quest.objects.filter(user_id=competition.user_id, upload_date__range=[competition.game_id.start_date,competition.game_id.end_date])
    competitor = Competitor.objects.get(competition_id=pk)

    #strftime("%Y-%m-%d") 사용해서 게임의 시작/종료일 변환
    start = competition.game_id.start_date.strftime("%Y-%m-%d")
    end = competition.game_id.end_date.strftime("%Y-%m-%d")

    #경쟁상대가 진행중인 퀘스트 목록 가져오기
    your_quest = Quest.objects.filter(user_id=competitor.competitor_id)
    filter_quest = your_quest.filter(upload_date__range=[competition.game_id.start_date,competition.game_id.end_date])

    #경쟁상대의 점수를 Competition에서 따로 가져올 수 없으므로 위에 필터한 퀘스트의 포인트들을 합산
    your_list = list(filter_quest.values('point'))
    your_sum = 0
    for i in range(len(your_list)):
        your_sum += your_list[i]['point']

    #Quest 입력하는 하는 로직, 운동/식단 중 고르고, 설명 내용 quest로 저장
    if request.method == "POST":
        quest_new = Quest.objects.create(
            game_id=competition.game_id,
            user_id=request.user,
            type=request.POST['type'],
            point= 3, #임시 설정
            content=request.POST['content'],

        )
        #Quest로 쌓인 포인트를 competition table에 저정하는 부분.
        # 그런데 여기서 Quest로 쌓인 점수를 game 기간동안 유저하고 있는 모든 competition에 더해야 되는지는 조원들에게 확인 필요
        competition.point += quest_new.point
        competition.save()

        return redirect('game_detail', competition.pk)
    return render(request, "game/game_detail.html", {'competitor':competitor,
                                                     'start':start, 'end': end,
                                                     'competition':competition,'quests':my_quest,'your_quests':filter_quest,
                                                     'your_point':your_sum})


def compete_followee(request,pk): #나를 경쟁상대로 지목한 유저의 competition을 pk로 받아온 페이지
    competition = Competition.objects.get(pk=pk)


    if request.method == 'POST':
        user = request.user

        new_competition = Competition.objects.create(
            game_id=competition.game_id,
            user_id=user,
        )
        competitor = Competitor.objects.create(
            competitor_id=competition.user_id,
            competition_id=new_competition
        )

        return redirect('game')

    return render(request, "game/compete_followee.html",{'competition':competition})




