from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView

from github_api.github_api import GithubApi
from .forms import RepoForm
from .models import Repo, GitAuthentication, Branch, Issue
from .forms import IssueForm
from .forms import PersonalTokenForm


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

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(HomeView, self).get(*args, **kwargs)
        else:
            return redirect('login')


def add_personal_token(request):
    message = ''
    if request.method == 'POST':
        form = PersonalTokenForm(request.POST)
        if form.is_valid():
            try:
                g = GithubApi(token=form.cleaned_data['access_token'])
                g.get_connection().get_user().login
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
    return render(request, 'add_personal_token.html', {'form': form, 'message': message})


def update_personal_token(request):
    message = ''
    current_user = request.user
    if request.method == 'POST':
        form = PersonalTokenForm(request.POST)
        if form.is_valid():
            try:
                g = GithubApi(token=form.cleaned_data['access_token'])
                if_token_ok = g.get_connection().get_user().login
            except:
                error = 'Wrong access token!'
                return render(request, 'add_personal_token.html', {'form': form, 'error': error})

            GitAuthentication.objects.filter(user=current_user).update(
                access_token=form.cleaned_data['access_token']
            )
            message = 'Your token has been successfully updated'

    else:
        form = PersonalTokenForm()
    return render(request, 'update_token.html', {'form': form, 'message': message})


def branches(request, pk):
    repo = get_object_or_404(Repo, pk=pk)
    branches = Branch.objects.filter(repo=repo).all()
    return render(request, 'branches.html', {'branches': branches})

@login_required
def scrum_board(request, pk):
    repo = get_object_or_404(Repo, pk=pk)
    token = GitAuthentication.objects.filter(user=request.user).first().access_token
    g = GithubApi(token=token)
    issues_by_label = {}
    labels = g.get_all_labels_in_repo(repo.name)

    for label in labels:
        issues_by_label[label] = list(Issue.objects.filter(repo_id=pk, label=label).all())

    return render(request, 'scrum_board.html', {'issues': issues_by_label, 'labels': labels})


def add_new_repo(request):
    success = ''
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
            if Repo.objects.filter(name=form.cleaned_data.get('name')):
                error = 'This repo has already been in your favourites'
                return render(request, 'add_new_repo.html', {'form': form, 'error': error})

            repo = form.save(commit=False)
            repo.name = form.cleaned_data.get('name')
            repo.save()
            repo.user.add(current_user)
            refresh_data(request, repo.id)
            success = 'Repo has been successfully added'

    else:
        form = RepoForm()
    return render(request, 'add_new_repo.html', {'form': form, 'success': success})


def remove_repo(request, pk):
    Repo.objects.filter(pk=pk).delete()
    Branch.objects.filter(repo_id=pk).delete()
    Issue.objects.filter(repo_id=pk).delete()
    return redirect('home')


def add_new_issue(request, pk):
    message = ''
    repo = get_object_or_404(Repo, pk=pk)
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            token = GitAuthentication.objects.filter(user=request.user).first().access_token
            g = GithubApi(token=token)
            try:
                g.create_new_issue(repo.name,
                                   form.cleaned_data.get('title'),
                                   form.cleaned_data.get('body'),
                                   form.cleaned_data.get('label'),
                                   form.cleaned_data.get('milestone'))
            except:
                return render(request, 'add_issue.html', {'form': form, 'error': 'Problem with connection'})

            issue = form.save(commit=False)
            issue.title = form.cleaned_data.get('title')
            issue.body = form.cleaned_data.get('body')
            issue.label = form.cleaned_data.get('label')
            issue.milestone = form.cleaned_data.get('milestone')
            issue.repo = repo
            issue.save()
            message = 'Your issue has been successfully added'

    else:
        form = IssueForm()
    return render(request, 'add_issue.html', {'form': form, 'message': message})


def get_issue_details(request, id):
    issue = Issue.objects.filter(id=id).first()
    return render(request, 'issue_details.html', {'issue': issue})


def add_branch(branch_name, pk):
    b = Branch()
    b.name = branch_name
    b.repo_id = pk
    b.save()


def add_issue(i, repo):
    new_issue = Issue()
    new_issue.title = i['title']
    new_issue.body = i['body']
    new_issue.label = i['label']
    new_issue.milestone = i['milestone']
    new_issue.assignee = i['assignee'].login if i['assignee'] is not None else None
    new_issue.number = i['number']
    new_issue.repo = repo
    new_issue.save()


def refresh_data(request, pk):
    repo = get_object_or_404(Repo, pk=pk)
    token = GitAuthentication.objects.filter(user=request.user).first().access_token
    g = GithubApi(token=token)
    branches = g.get_names_of_branch(repo.name)
    issues = g.get_all_issues(repo.name)
    Branch.objects.filter(repo=repo).delete()
    Issue.objects.filter(repo=repo).delete()

    for branch_name in branches:
        add_branch(branch_name, pk)

    for i in issues:
        add_issue(i, repo)

    return redirect('home')
