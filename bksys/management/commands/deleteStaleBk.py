from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import requests
from bksys.models import * 

class Command(BaseCommand):
    def handle(self, *args, **options):
    	bookings.objects.removeStaleBookings()
        
