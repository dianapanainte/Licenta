from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Player(models.Model):
    name = models.CharField(max_length=100)
    player_id = models.AutoField(primary_key=True)
    date_of_birth = models.CharField(max_length=50)
    height = models.CharField(max_length=10)
    hand = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    ranking = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class RecentTournamentManager(models.Manager):
    def past_tournaments(self):
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month

        tournaments = self.all()
        filtered_tournaments = []

        for tournament in tournaments:
            try:
                start_date_str = tournament.date.split('-')[0].strip() + f", {current_year}"
                start_date = datetime.datetime.strptime(start_date_str, '%b %d, %Y').date()

                if (start_date.year < current_year) or (
                        start_date.year == current_year and start_date.month <= current_month):
                    tournament.start_date_obj = start_date
                    filtered_tournaments.append(tournament)
            except ValueError:
                continue

        filtered_tournaments.sort(key=lambda x: x.start_date_obj, reverse=True)

        return filtered_tournaments

    def future_tournaments(self):
        today = timezone.now().date()
        current_year = today.year
        next_month = today.replace(day=1, month=today.month + 1)

        tournaments = self.all()
        filtered_tournaments = []

        for tournament in tournaments:
            try:
                end_date_str = tournament.date.split('-')[-1].strip()
                end_date = datetime.datetime.strptime(end_date_str, '%b %d, %Y').date()

                # Check if the tournament end date is from July onwards
                if end_date.month >= 7:
                    tournament.end_date_obj = end_date
                    filtered_tournaments.append(tournament)
            except ValueError:
                continue

        filtered_tournaments.sort(key=lambda x: x.end_date_obj)

        return filtered_tournaments


class Tournament(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournaments')
    date = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    opponent_player = models.CharField(max_length=100)
    opponent_rank = models.CharField(max_length=10)
    location = models.CharField(max_length=100, blank=True, null=True)
    surface = models.CharField(max_length=50)
    round = models.CharField(max_length=50)
    score = models.CharField(max_length=50)
    result = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} won by {self.player.name} on {self.surface}"


class RecentTournament(models.Model):
    date = models.CharField(max_length=50)
    surface = models.CharField(max_length=10)
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    objects = RecentTournamentManager()

    def __str__(self):
        return f"Tournament {self.title} on + {self.date}"


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.player.name}"


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    height = models.CharField(max_length=10)
    hand = models.CharField(max_length=10)
    rank = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    wins_semester = models.CharField(max_length=10)
    losses_semester = models.CharField(max_length=10)
    wins_year = models.CharField(max_length=10)
    losses_year = models.CharField(max_length=10)
    wins_clay = models.CharField(max_length=10)
    losses_clay = models.CharField(max_length=10)
    wins_hard = models.CharField(max_length=10)
    losses_hard = models.CharField(max_length=10)
    wins_grass = models.CharField(max_length=10)
    losses_grass = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.player} - stats"

