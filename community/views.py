from asyncio.proactor_events import _ProactorBasePipeTransport
from audioop import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

# 2022.03.26 최승대 작성
# 템플릿 언어 ex) back-end -> front-end
# 1. 커뮤니티 페이지 함수 : all_post -> posts
# 2. 포스트 페이지 함수 : all_post -> posts
# 3. 포스트 수정 함수 : posts -> post
# 4. 세부 페이지 함수 : post -> post / post_comment -> comments

######### 커뮤니티 페이지 함수 #########
def community(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            all_post = Post.objects.all().order_by('-created_at')
            return render(request, 'community/community.html', {'posts': all_post})
        else:
            return redirect('/')

######### 포스트 페이지 함수 #########
@login_required
def post(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return render(request, 'community/community_post.html')
        else:
            return redirect('/')
    elif request.method == "POST":
        user = request.user
        content = request.POST.get('my-content', '')
        print(content)
        tags = request.POST.get('tag', '').split('#')
        if content == '':
            all_post = Post.objects.all().order_by('-created_at')
            return render(request, 'community/community_post.html', {'error': '공백은 제출할 수 없습니다.', 'posts': all_post})
        else:
            my_post = Post.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip('#')
                if tag != '':
                    my_post.tags.add(tag)
            my_post.save()
        return redirect('/community')

######### 포스트 수정 함수 #########
@login_required
def update(request, id):
    if request.method == "GET":
        posts = Post.objects.get(id=id)
        return render(request, 'community/community_edit.html', {'post': posts})
    
    elif request.method == "POST":
        user = request.user
        post = Post.objects.get(id=id)
        post.author = user
        post.content = request.POST.get('content_edit')
        post.save()
        return redirect('/community/' + str(id))

######### 포스트 삭제 함수 #########
@login_required
def post_delete(request, id):
    my_post = Post.objects.get(id=id)
    my_post.delete()
    return redirect('/community')

######### 댓글 달 때 세부 페이지로 이동 함수 #########
@login_required
def post_detail(request, id):
    post = Post.objects.get(id=id)
    post_comment = Comment.objects.filter(post_id=id).order_by('-created_at')
    return render(request, 'community/community_detail.html', {'post': post, 'comments': post_comment})

######### 댓글 작성 함수 #########
@login_required
def write_comment(request, id):
    if request.method == "POST":
        comment = request.POST.get('comment', '')
        current_post = Post.objects.get(id=id)
        PC = Comment()
        PC.comment = comment
        PC.author = request.user
        PC.post = current_post
        PC.save()
    return redirect('/community/' + str(id))

######### 댓글 수정 함수 #########
@login_required
def comment_update(request, id):
    if request.method == "POST":
        comment = Comment.objects.get(id=id)
        comment.comment = request.POST['comment_content']
        current_post = comment.post.id
        comment.save()
    return redirect('/community/' + str(current_post))
    
######### 댓글 삭제 함수 #########
@login_required
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    current_post = comment.post.id
    comment.delete()
    return redirect('/community/' + str(current_post))

######### 포스트 좋아요 함수 #########
@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    return redirect('/community/')

######### 댓글 좋아요 함수 #########
@login_required
def comment_like(request, id):
    comment = Comment.objects.get(id=id)
    current_post = comment.post.id
    if request.user in comment.like.all():
        comment.like.remove(request.user)
        comment.like_count -= 1
        comment.save()
    else:
        comment.like.add(request.user)
        comment.like_count += 1
        comment.save()
    return redirect('/community/' + str(current_post))

######### 태그 기능 클래스 #########
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context