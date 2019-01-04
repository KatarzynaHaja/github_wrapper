from django import forms
from .models import Repos

class ReposForm(forms.ModelForm):

    class Meta:
        model = Repos
        fields = ('name',)