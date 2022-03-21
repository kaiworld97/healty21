from django.shortcuts import render,redirect
from user.models import UserModel
from .models import Group,Game, Competition, Competitor
from django.contrib.auth.decorators import login_required
import datetime



# Create your views here.
def index(request):

    return render(request, 'game/index.html')

def game(request):
    my_competition = Competition.objects.filter(user_id=request.user).values('game_id')
    print(my_competition)
    # games = Game.objects.filter(title__startswith=request.user.nick_name)
    games = Game.objects.filter(pk__in=my_competition)
    competitors = Competitor.objects.filter(competitor_id=request.user)
    competitions = Competition.objects.filter(pk__in=competitors)
    return render(request, "game/competition.html",{'games':games,'competitions':competitions})

@login_required(login_url='signin')
def set_goal(request):
    groups = Group.objects.all()
    return render(request, "game/set_goal.html",{'groups':groups})


def matching(request,pk):
    group = Group.objects.get(pk=pk)
    members = UserModel.objects.filter(group_id=pk)

    if request.method == 'POST':
        user=UserModel.objects.get(username=request.user)
        print(group)
        user.group_id= group
        print(user.group_id)
        user.save()

        user_competitor = request.POST['nick_name']
        end_date = datetime.date.today() + datetime.timedelta(weeks=3)
        game = Game.objects.create(
            group_id=group,
            title=f'{user.nick_name} vs {user_competitor}',
            status = 'True',
            end_date= end_date,
        )
        competition = Competition.objects.create(
            game_id= game,
            user_id= user,

        )
        competitor = Competitor.objects.create(
            competitor_id=UserModel.objects.get(nick_name=user_competitor),
            competition_id=competition
        )

        return redirect('game')

    return render(request, "game/matching.html", {'members': members,'group':group})

def game_detail(request,pk):
    game = Game.objects.get(pk=pk)
    competition = Competition.objects.get(game_id=pk)
    competitor = Competitor.objects.filter(competition_id=competition).values('competitor_id')
    competitor_nickname= UserModel.objects.get(pk__in=competitor)
    date_count= game.start_date



    return render(request, "game/game_detail.html", {'competitor':competitor_nickname})

def compete_followee(request,pk):

    return render(request, "game/compete_followee.html")




