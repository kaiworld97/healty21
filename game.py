import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from game.models import Game, UserGroup, User
import datetime

# groups = [{'goal': 3, 'level': 1}, {'goal': 3, 'level': 2}, {'goal': 3, 'level': 3}, {'goal': 5, 'level': 1},
#           {'goal': 5, 'level': 2}, {'goal': 5, 'level': 3}]

group = [{'goal': 3, 'level': 1}, {'goal': 5, 'level': 1}]


def make_group():
    for group in groups:
        user_group = UserGroup()
        user_group.goal = group['goal']
        user_group.level = group['level']
        user_group.save()


def make_game():
    user_groups = UserGroup.objects.all()
    for user_group in user_groups:
        game = Game()
        game.group = user_group
        game.title = f'{user_group}의 경쟁'
        game.end_date = datetime.datetime.now() + datetime.timedelta(days=21)
        game.save()


def start_game():
    games = Game.objects.all().order_by('start_date')[:6]
    games.update(status=True)
    User.objects.all().update(competition_activate=False)


def end_game():
    games = Game.objects.filter(status=True)
    games.update(status=False)


def days_gone():
    User.objects.all().update(view_eval=False)
    games = Game.objects.filter(status=True)
    # 몇일 진행중 계산
    day = int(
        str(datetime.datetime.now() - datetime.datetime.fromtimestamp(game[0].start_date.timestamp())).split(' ')[0])
    games.update(day=day)


make_group()
make_game()
