import dashboard.tennis as tennis

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, PlayerForm, CustomPlayerForm
from django.contrib.auth.decorators import login_required
from .models import RecentTournament, Player, Tournament, PlayerStat, SurfaceTournament
from .models import UserFavorite
from .forms import FavoriteForm


@login_required(login_url='/login/')
def dashboard_view(request):
    past_tournaments = RecentTournament.objects.past_tournaments()
    future_tournaments = RecentTournament.objects.future_tournaments()
    players = Player.objects.all().order_by('name')
    tournaments_from_dataset = SurfaceTournament.objects.all().order_by('tournament')
    if request.method == 'POST':
        form = CustomPlayerForm(request.POST)
        if form.is_valid():
            player1_id = form.cleaned_data['player1']
            player2_id = form.cleaned_data['player2']
            tournament_id = form.cleaned_data['tournament']

            if player1_id == player2_id:
                form.add_error(None, "Players must be different!")
            else:
                player1 = Player.objects.get(player_id=player1_id)
                player2 = Player.objects.get(player_id=player2_id)
                tournament = SurfaceTournament.objects.get(id=tournament_id)
                surface = tournament.surface
                round = form.cleaned_data['round']
                player1_stats = PlayerStat.objects.get(id=player1_id)
                player2_stats = PlayerStat.objects.get(id=player2_id)
                tennis.predict(player1, player2, tournament, surface, round, player1_stats, player2_stats)
                print(f"Tournament: {tournament.tournament}, Round: {round}")
                print(player1.name, player2.name)
    else:
        form = CustomPlayerForm()

    return render(request, 'dashboard/dashboard.html',
                  {'tournaments': past_tournaments, 'future_tournaments': future_tournaments, 'players': players,
                   'form': form, 'all_tournaments': tournaments_from_dataset})


@login_required
def add_favourite_view(request):
    if request.method == 'POST':
        form = FavoriteForm(request.POST, user=request.user)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.save()
            return redirect('favourites')
    else:
        form = FavoriteForm(user=request.user)
    return render(request, 'dashboard/add_favourite.html', {'form': form})


@login_required(login_url='/login/')
def favourites_view(request):
    user_favorites = UserFavorite.objects.filter(user=request.user)
    matches = Tournament.objects.all()
    stats = PlayerStat.objects.all()
    return render(request, 'dashboard/favourites.html',
                  {'user_favorites': user_favorites, 'matches': matches, 'stats': stats})


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
