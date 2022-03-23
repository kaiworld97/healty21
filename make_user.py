import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from user.models import User
from game.models import Quest, Game


for i in range(1, 6):
    user = User()
    user.username = f'홍채영{i}'
    user.email = f'hcy{i}@gmail.com'
    user.password = '1111'
    user.save()
    game = Game.objects.get(id=3)
    quest = Quest()
    quest.user = user
    quest.game = game
    quest.type = 'workout'
    quest.point = 5
    quest.content = f'content{i}'
    quest.photo = 'https://img.freepik.com/free-photo/full-length-side-view-of-focused-slim-asian-girl-doing-fitness-training-female-athlete-clasp-hands-together-and-perform-squats-exercises-with-stretching-resistance-band-workout-equipment_1258-21439.jpg'
    quest.save()
    quest1 = Quest()
    quest1.user = user
    quest1.game = game
    quest1.type = 'food'
    quest1.point = 5
    quest1.content = f'content{i}'
    quest1.photo = 'https://image.newdaily.co.kr/site/data/img/2021/01/10/2021011000024_0.jpg'
    quest1.save()


