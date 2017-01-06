from fabric.api import *

env.hosts = ['yourdomain.com']

def update_django_project():
    """ Updates the remote django project.
    """
    with cd('/home/main/BKSYSDEPLOY/bookingsystem'):
        run('git pull')
        with prefix('source /home/main/BKSYSDEPLOY/bin/activate'):
            run('pip install -r requirements.txt')
            run('python manage.py syncdb')
            run('python manage.py migrate') # if you use south
            run('python manage.py collectstatic --noinput')

def restart_webserver():
    """ Restarts remote nginx and uwsgi.
    """
    sudo("service uwsgi restart")
    sudo("/etc/init.d/nginx restart")

def deploy():
    update_django_project()
    restart_webserver()