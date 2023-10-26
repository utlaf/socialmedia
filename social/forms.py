from django import forms
from .models import Post,Profile
from .models import Comment
from django.contrib.auth.forms import PasswordResetForm

# from .models import Comment
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']



class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['text', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )