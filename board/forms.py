from django.contrib.auth.models import User
from django import forms
from .models import Topic, Post

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000, help_text="No more than 4000 characters")

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(help_text=None)
    
    class Meta:
        model = User
        fields = ['username', 'password']
    

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['message', ]