# feed/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile
from .forms import UserRegisterForm, ProfileEditForm, PostForm, CommentForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('feed:home')
    else:
        form = UserRegisterForm()
    return render(request, 'feed/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('feed:login')

@login_required
def home(request):
    followed_users_profiles = request.user.following.all()
    followed_users_ids = [profile.user.id for profile in followed_users_profiles]
    followed_users_ids.append(request.user.id)
    posts = Post.objects.filter(author__id__in=followed_users_ids)
    return render(request, 'feed/home.html', {'posts': posts})

def explore(request):
    posts = Post.objects.all()
    return render(request, 'feed/explore.html', {'posts': posts})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    is_following = request.user.is_authenticated and request.user.following.filter(user=user).exists()
    return render(request, 'feed/profile.html', {'profile_user': user, 'posts': posts, 'is_following': is_following})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('feed:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'feed/edit_profile.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed:home')
    else:
        form = PostForm()
    return render(request, 'feed/create_post.html', {'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('feed:post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'feed/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'feed:home'))

@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = user_to_follow.profile
    if profile_to_follow in request.user.following.all():
        request.user.following.remove(profile_to_follow)
    else:
        request.user.following.add(profile_to_follow)
    return redirect('feed:profile', username=username)