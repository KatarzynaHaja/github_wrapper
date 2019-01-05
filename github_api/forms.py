from django import forms
from .models import Repos
from .models import Issuses

class ReposForm(forms.ModelForm):

    class Meta:
        model = Repos
        fields = ('name',)


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issuses
        fields = ('title', 'body', 'label', 'milestone','assignee')