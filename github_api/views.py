from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from github_api.forms import SignUpForm

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration_form.html', {'form': form})