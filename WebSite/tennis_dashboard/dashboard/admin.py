from django.contrib import admin
from .models import Player, Tournament, RecentTournament, PlayerStat, SurfaceTournament

admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(RecentTournament)
admin.site.register(PlayerStat)
admin.site.register(SurfaceTournament)
