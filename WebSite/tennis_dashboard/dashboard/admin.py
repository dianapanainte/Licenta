from django.contrib import admin
from .models import Player, Tournament, RecentTournament, PlayerStat

admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(RecentTournament)
admin.site.register(PlayerStat)
