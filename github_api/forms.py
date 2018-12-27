from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from github_api.models import MyUser


class SignUpForm(UserCreationForm):
    # github_name = forms.CharField(max_length=30, required=True)
    github_password =forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = MyUser
        fields = ('name','github_name', 'github_password', 'password1','password2', 'email' )