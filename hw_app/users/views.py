from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


# Create your views here.
@login_required
def logout_user(request):
    logout(request)
    return redirect(to='hw_ten_app:main')


def signup_user(request):
    if request.user.is_authenticated:
        return redirect(to='hw_ten_app:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='hw_ten_app:main')
        else:
            return render(request, 'users/signup.html', {'form': form})

    return render(request, 'users/signup.html', {'form': RegisterForm()})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='hw_ten_app:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})
