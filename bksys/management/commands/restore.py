from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('dbrestore')
