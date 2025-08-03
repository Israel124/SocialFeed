from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'feed'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('', auth_views.LoginView.as_view(template_name='feed/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('create_story/', views.create_story, name='create_story'),
]
