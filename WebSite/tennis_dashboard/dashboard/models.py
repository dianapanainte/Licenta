from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"Tournament {self.title} on + {self.date}"


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.player.name}"
