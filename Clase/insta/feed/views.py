#feed/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile
from django.contrib import messages
from .forms import UserRegisterForm, ProfileEditForm, PostForm, CommentForm
from .forms import ProfileForm, StoryForm
from .models import Post, Comment, Profile, Story

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
    query = request.GET.get('q')
    users = None
    posts = Post.objects.all().order_by('-created_at')
    
    if query:
        # Buscar usuarios cuyo username contenga la query (case-insensitive)
        users = User.objects.filter(username__icontains=query)
        # También buscar posts que contengan la query en el caption
        posts = posts.filter(caption__icontains=query)
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    context = {
        'posts': posts,
        'users': users,
        'query': query,
    }
    return render(request, 'feed/explore.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    is_following = request.user.is_authenticated and request.user.following.filter(user=user).exists()
    return render(request, 'feed/profile.html', {'profile_user': user, 'posts': posts, 'is_following': is_following})

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    
    # Calcular estadísticas
    post_count = Post.objects.filter(author=user).count()
    follower_count = profile.followers.count()
    following_count = user.following.count()
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redireccionar a perfil con mensaje de éxito
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'user': user
    }
    return render(request, 'feed/edit_profile.html', context)

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
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('feed:home')
    else:
        form = StoryForm()
    return render(request, 'feed/create_story.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Verificar que el usuario es el autor de la publicación
    if post.author != request.user:
        messages.error(request, "No tienes permiso para realizar esta acción.")
        return redirect('feed:post_detail', pk=post.pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "La publicación ha sido eliminada.")
        return redirect('feed:home')
    
    return redirect('feed:post_detail', pk=post.pk)

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