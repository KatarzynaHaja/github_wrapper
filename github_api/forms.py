from django import forms
from .models import Repo
from .models import Issue
from .models import GitAuthentication

class RepoForm(forms.ModelForm):

    class Meta:
        model = Repo
        fields = ('name',)


class IssueForm(forms.ModelForm):
    milestone = forms.CharField(required=False)

    class Meta:
        model = Issue
        fields = ('title', 'body', 'label', 'milestone')


class PersonalTokenForm(forms.ModelForm):

    class Meta:
        model = GitAuthentication
        fields = ('access_token',)