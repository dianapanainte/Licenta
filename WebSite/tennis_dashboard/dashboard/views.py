from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import RecentTournament


@login_required(login_url='/login/')
def dashboard_view(request):
    tournaments = RecentTournament.objects.all()
    return render(request, 'dashboard/dashboard.html', {'tournaments': tournaments})


@login_required(login_url='/login/')
def favourites_view(request):
    return render(request, 'dashboard/favourites.html')


@login_required(login_url='/login/')
def account_view(request):
    return render(request, 'dashboard/account.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/signup.html', {'form': form})


@login_required
def delete_own_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('account_deleted')

    return render(request, 'dashboard/delete_own_account.html')


@login_required
def account_deleted_view(request):
    return render(request, 'dashboard/account_deleted.html')


def login_first_view(request):
    return render(request, 'dashboard/login_first_please.html')
