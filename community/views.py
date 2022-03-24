from audioop import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required

def community(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            all_post = Post.objects.all().order_by('-created_at')
            return render(request, 'community/community.html', {'posts': all_post})
        else:
            return redirect('/')

def post(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return render(request, 'community/community_post.html')
        else:
            return redirect('/')
    elif request.method == "POST":
        user = request.user
        post = Post()
        post.author = user
        post.title = request.POST.get('content_title', '')
        post.content = request.POST.get('my-content', '')
        post.save()
        return redirect('/community')

@login_required
def update(request, id):
    if request.method == "GET":
        post = Post.objects.get(id=id)
        return render(request, 'community/community_edit.html', {'post': post})
    
    elif request.method == "POST":
        user = request.user
        post = Post.objects.get(id=id)
        post.author = user
        post.content = request.POST.get('content_edit')
        post.save()
        return redirect('/community/' + str(id))

@login_required
def post_delete(request, id):
    my_post = Post.objects.get(id=id)
    my_post.delete()
    return redirect('/community')

@login_required
def post_detail(request, id):
    post = Post.objects.get(id=id)
    post_comment = Comment.objects.filter(post_id=id).order_by('-created_at')
    return render(request, 'community/community_detail.html', {'post': post, 'comments': post_comment})

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

@login_required
def comment_update(request, id):
    if request.method == "POST":
        comment = Comment.objects.get(id=id)
        current_post = comment.post.id
        comment.comment = request.POST['comment_content']
        comment.save()
    return redirect('/community/' + str(current_post))
    
@login_required
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    current_post = comment.post.id
    comment.delete()
    return redirect('/community/' + str(current_post))

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