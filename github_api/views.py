from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView

from github_api.github_api import  GithubApi
from .forms import ReposForm
from .models import Repos, Branches
from .forms import IssueForm


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
            current_user = request.user
            repo = form.save(commit=False)
            repo.name = form.cleaned_data.get('name')
            repo.save()
            repo.user.add(current_user)

    else:
        form = ReposForm()
    return render(request, 'add_new_repo.html', {'form': form})


def add_new_issue(request, pk):
    repo = get_object_or_404(Repos, pk=pk)
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            g = GithubApi("KatarzynaHaja", 'Studia123')
            g.create_new_issue(form.cleaned_data.get('title'),
                               form.cleaned_data.get('body'),
                               form.cleaned_data.get('label'),
                               form.cleaned_data.get('milestone'),
                               form.cleaned_data.get('assignee'))
            issue = form.save(commit=False)
            issue.title = form.cleaned_data.get('title')
            issue.body = form.cleaned_data.get('body')
            issue.label = form.cleaned_data.get('label')
            issue.milestone = form.cleaned_data.get('milestone')
            issue.assignee = form.cleaned_data.get('assignee')
            issue.repo = repo
            issue.save()


    else:
        form = IssueForm()
    return render(request, 'add_issue.html', {'form': form})


class HomeView(ListView):
    model = Repos
    paginate_by = 5
    template_name = 'home.html'

    def get_queryset(self):
        return Repos.objects.filter(user=self.request.user)

    # def get_context_data(self,**kwargs):
    #     query_results = Repos.objects.filter(user=kwargs.user)
    #     pass
    #     return render(kwargs, 'home.html', {'query_results': query_results})


def get_repo_details(request, pk):
    repo = get_object_or_404(Repos, pk=pk)
    pass
    return render(request, 'repo_details.html', {'repo': repo})