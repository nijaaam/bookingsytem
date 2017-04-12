from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import requests, socket
from django.db import connection
import paramiko, subprocess, os

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
	    uwsgi.start()
            r = requests.head('http://localhost')
            if r != 200:
                os.system('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')
        except:
            os.system('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')
        #self.testMySQLConnection()

        
    def testMySQLConnection(self):
        try:
            soc = socket.create_connection(('mysql2704.cloudapp.net','3306'),5)
            soc.close()
        except:
            host = 'mysql2704.cloudapp.net'
            user = "main"
            keyLoc = '/etc/keys/mysql'
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username="main",key_filename=keyLoc)
            stdin, stdout, stderr = client.exec_command('sudo service mysql restart')
            print "stderr: ", stderr.readlines()
            print "pwd: ", stdout.readlines()
        



