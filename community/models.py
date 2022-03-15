from multiprocessing import AuthenticationError
from telnetlib import STATUS
from turtle import title
from django.db import models
from user.models import UserModel

class Post(models.Model):
    class Meta:
        db_table = "community"
    
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=256)
    content = models.TextField(max_length=256) 
    title = models.TextField(max_length=256)
    count_comment = models.IntegerField(default=0)

    # 2022.03.14
    # status, type 필드는 무엇을 의미하는지 => status는 임시저장되어있는지 확인하는 것, type은 공유한 글인지 아닌지
    # 각 레코드들이 기준에 잘 들어갔는지 확인 필요합니다.
    # count_comment가 댓글 조회수를 의미하는 것이라면 Post 테이블에 없어도 되지 않는 것인지 확인 필요합니다. 만약 포스팅된 글의 조회수라면 필드명 정정해야할 것 같습니다.

class Comment(models.Model):
    class Meta:
        db_table = "comment"
    
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=256)
    count_comment = models.IntegerField(default=0)