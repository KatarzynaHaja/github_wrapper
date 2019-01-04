from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from github_api.github_api import  GithubApi
from .forms import ReposForm
from .models import Repos

@login_required
def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            g = GithubApi(username, raw_password)
            try:
                t = g.get_connection().get_user().login
                form.save()
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'registration_form.html', {'form':form,'error':'ALOALO'})

    else:
        form = UserCreationForm()
    return render(request, 'registration_form.html', {'form': form})


def add_new_repo(request):
    if request.method == "POST":
        form = ReposForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.name = form.cleaned_data.get('name')
            repo.save()
    else:
        form = ReposForm()
    return render(request, 'add_new_repo.html', {'form': form})

def get_repos(request):
    query_results = Repos.objects.all()
    pass
    return render(request, 'home.html', {'query_results':query_results})