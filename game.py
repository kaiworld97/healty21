import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from game.models import Game, UserGroup
import datetime

groups = [{'goal': 3, 'level': 1}, {'goal': 3, 'level': 2}, {'goal': 3, 'level': 3}, {'goal': 5, 'level': 1},
          {'goal': 5, 'level': 2}, {'goal': 5, 'level': 3}]


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
    games = Game.objects.filter()
    games.save()


def end_game():
    games = Game.objects.filter()
    games.save()


def days_gone():
    game = Game.objects.filter()
    # 몇일 진행중 계산
    day = int(
        str(datetime.datetime.now() - datetime.datetime.fromtimestamp(game[0].start_date.timestamp())).split(' ')[0])
    game.update(day=day)


make_group()
make_game()
