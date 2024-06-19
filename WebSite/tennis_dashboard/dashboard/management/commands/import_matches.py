import json
import sys
from os import path

from django.core.management.base import BaseCommand
sys.path.append(path.abspath('../tennis_dashboard'))
from dashboard.models import Tournament, Player


class Command(BaseCommand):
    help = 'Imports tournament data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to be imported')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file) as file:
            data = json.load(file)
            for entry in data:
                player_name = entry['name']
                player = Player.objects.get(name=player_name)
                Tournament.objects.create(
                    player=player,
                    date=entry['date'],
                    name=entry['tournament'],
                    opponent_player=entry['opponent_player'],
                    opponent_rank=entry['opponent_rank'],
                    location=entry['location'],
                    surface=entry['surface'],
                    round=entry['round'],
                    score=entry['score'],
                    result=entry['result']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
