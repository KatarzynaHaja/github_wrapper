from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView

from github_api.github_api import  GithubApi
from .forms import RepoForm
from .models import Repo, GitAuthentication, Branch
from .forms import IssueForm
from .forms import PersonalTokenForm



@login_required
def home(request):
    return render(request, 'home.html')


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()
    return render(request, 'registration_form.html', {'form': form})

@login_required
def add_new_repo(request):
    success=''
    error=''
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            current_user = request.user
            token = GitAuthentication.objects.filter(user=current_user).first().access_token
            g = GithubApi(token=token)
            try:
                g.get_repo_by_name(form.cleaned_data['name'])
            except:
                error = "This repo doesn't exist"
                return render(request, 'add_new_repo.html', {'form': form, 'error': error})

            repo = form.save(commit=False)
            repo.name = form.cleaned_data.get('name')
            repo.save()
            repo.user.add(current_user)
            success = 'Repo has been successfully added'

    else:
        form = RepoForm()
    return render(request, 'add_new_repo.html', {'form': form, 'success':success})


def add_new_issue(request, pk):
    repo = get_object_or_404(Repo, pk=pk)
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            token = GitAuthentication.objects.filter(user = request.user).first().access_token
            g = GithubApi(token=token)
            g.create_new_issue(repo.name,
                               form.cleaned_data.get('title'),
                               form.cleaned_data.get('body'),
                               form.cleaned_data.get('label'),
                               form.cleaned_data.get('milestone'))

            issue = form.save(commit=False)
            issue.title = form.cleaned_data.get('title')
            issue.body = form.cleaned_data.get('body')
            issue.label = form.cleaned_data.get('label')
            issue.milestone = form.cleaned_data.get('milestone')
            issue.repo = repo
            issue.save()

    else:
        form = IssueForm()
    return render(request, 'add_issue.html', {'form': form})


def add_personal_token(request):
    message = ''
    if request.method == 'POST':
        form = PersonalTokenForm(request.POST)
        if form.is_valid():
            try:
                g = GithubApi(token=form.cleaned_data['access_token'])
                if_token_ok = g.get_connection().get_user().login
            except:
                error = 'Wrong access token!'
                return render(request, 'add_personal_token.html', {'form': form, 'error': error})
            token = form.save(commit=False)
            token.access_token = form.cleaned_data.get('access_token')
            token.save()
            token.user.add(request.user)
            message = 'Your token has been successfully added'

    else:
        form = PersonalTokenForm()
    return render(request, 'add_personal_token.html', {'form':form, 'message': message})


class HomeView(ListView):
    model = Repo
    paginate_by = 5
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        access = None
        context = super().get_context_data(**kwargs)
        token = GitAuthentication.objects.filter(user=self.request.user).first()
        if token:
            access = True
        context['access'] = access
        return context

    def get_queryset(self):
        return Repo.objects.filter(user=self.request.user)


def get_repo_details(request, pk):
    repo = get_object_or_404(Repo, pk=pk)
    return render(request, 'repo_details.html', {'repo': repo})


def refresh_data(request, pk):
    repo = get_object_or_404(Repo, pk=pk)
    token = GitAuthentication.objects.filter(user=request.user).first().access_token
    g = GithubApi(token=token)
    branches = g.get_names_of_branch()
    for branch_name in branches:
        b = Branch()
        b.name = branch_name
        b.repo_id = pk
        b.save()



