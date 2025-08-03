from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Story

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_picture']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Añade un comentario...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']  # Usa el nombre correcto del campo

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a caption...'}),
        }
