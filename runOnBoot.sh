#!/usr/bin/env bash

cd /home/main/BKSYSDEPLOY
source bin/activate
/home/main/BKSYSDEPLOY/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
export DJANGO_SETTINGS_MODULE=bookingsystem.production
exit 0


