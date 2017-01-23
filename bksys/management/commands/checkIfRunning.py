from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            r = requests.head('http://localhost:8000')
            if r != 200:
                call_command('runserver')
        except:
            call_command('runserver')
