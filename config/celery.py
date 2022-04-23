from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") ## 우측의 batch는 독자의 프로젝트이름으로 대체

app = Celery('config', broker='redis://localhost:6379/0') #이 또한 독자의 프로젝트로 댁체

app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
app.conf.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
)


# @app.task(bind=True) # 잘 되고 있나 확인하기 위해 설정
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
#
#
# app.conf.beat_schedule = { ## 셀러리 비트로서 일정 시간마다 업무를 주어주도록 설정
#     'add': {
#         'task': 'game.tasks.add',
#         'schedule': crontab(minute=1, hour=0),
#     },
# }
