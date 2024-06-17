from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)
    player_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField()
    height = models.CharField(max_length=10)
    hand = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tournaments')
    date = models.DateField()
    name = models.CharField(max_length=100)
    opponent_player = models.CharField(max_length=100)
    opponent_rank = models.IntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)
    surface = models.CharField(max_length=50)  # e.g., Grass, Clay, Hard
    round = models.CharField(max_length=50)  # e.g., Final, Semi-final
    score = models.CharField(max_length=50)  # e.g., 6-4, 6-7, 7-5
    result = models.BooleanField()  # True for win, False for loss

    def __str__(self):
        return f"{self.name} won by {self.player.name} on {self.surface}"


class RecentTournament(models.Model):
    date = models.CharField(max_length=50)
    surface = models.CharField(max_length=10)
    location = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Tournament {self.title} on + {self.date}"
