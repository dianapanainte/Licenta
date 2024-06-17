# your_app/management/commands/import_tournaments.py
import json
import sys
from os import path

from django.core.management.base import BaseCommand
sys.path.append(path.abspath('../tennis_dashboard'))
from dashboard.models import RecentTournament


class Command(BaseCommand):
    help = 'Imports tournament data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to be imported')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        with open(json_file) as file:
            data = json.load(file)
            for entry in data:
                RecentTournament.objects.create(
                    date=entry['date'],
                    surface=entry['surface'],
                    location=entry['location'],
                    title=entry['title']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
