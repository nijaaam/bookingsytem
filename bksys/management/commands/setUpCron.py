from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from crontab import CronTab

class Command(BaseCommand):
	def handle(self, *args, **options):
		mem_cron = CronTab(tab="""
			@midnight /home/nijam/Desktop/bookingsystem manage.py runserver
		""")
		mem_cron.write()
		print mem_cron.render()
        
