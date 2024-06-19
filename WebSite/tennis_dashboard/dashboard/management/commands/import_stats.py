import json
import sys
from os import path

from django.core.management.base import BaseCommand
sys.path.append(path.abspath('../tennis_dashboard'))
from dashboard.models import PlayerStats, Player


class Command(BaseCommand):
    help = 'Imports tournament data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to be imported')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file) as file:
            data = json.load(file)
            for entry in data:
                try:
                    player_name = entry['name']
                    player = Player.objects.get(name=player_name)
                    PlayerStats.objects.create(
                        player=player,
                        height=entry['height'],
                        hand=entry['hand'],
                        rank=entry['rank'],
                        age=entry['age'],
                        wins_semester=entry['wins_semester'],
                        losses_semester=entry['losses_semester'],
                        wins_year=entry['wins_year'],
                        losses_year=entry['losses_year'],
                        wins_clay=entry['wins_clay'],
                        losses_clay=entry['losses_clay'],
                        wins_hard=entry['wins_hard'],
                        losses_hard=entry['losses_hard'],
                        wins_grass=entry['wins_grass'],
                        losses_grass=entry['losses_grass']
                    )
                except Player.DoesNotExist:
                    continue

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
