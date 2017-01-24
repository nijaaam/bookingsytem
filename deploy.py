#!/usr/bin/env python
from deployer.client import start
from deployer.node import Node, required_property
from deployer.utils import esc1
from deployer.host import SSHHost
from deployer.exceptions import ActionException

home = '/home/main/'
ip = 'bksystesting1818.cloudapp.net'
project_name = "bookingsystem/"
virtualenv = "BKSYSDEPLOY/"
project_dir = home + virtualenv + project_name
repo = 'https://github.com/nijaaam/bookingsystem.git'
keyLocation = '/home/nijam/Desktop/keys/bookingsystem'
cronLog = '/var/log/cronjobs/'

class VirtualEnv(Node):
    location = required_property()
    requirements_files = []
    packages = []

    @property
    def activate_cmd(self):
        return  '. %sbin/activate' % self.location

    def install_requirements(self):
        with self.hosts.prefix(self.activate_cmd):
            for f in self.requirements_files:
                self.hosts.sudo("pip install -r '%s' " % esc1(f))

    def install_package(self, name):
        with self.hosts.prefix(self.activate_cmd):
            self.hosts.run("pip install '%s'" % name)

    def setup_env(self):
        for p in self.packages:
            self.install_package(p)
        self.install_requirements()

    def run_management_command(self, command):
        with self.hosts.prefix(self.activate_cmd):
            with self.hosts.cd(project_dir):
                self.hosts.run('./manage.py %s' % command)

    def run_uwsgi(self):
        with self.hosts.prefix(self.activate_cmd):
            with self.hosts.cd(project_dir):
                self.hosts.run('uwsgi start_app.ini')

    def collectstatic(self):
        self.run_management_command('collectstatic --clear --noinput')

    def update_database(self):
        self.run_management_command('migrate --noinput')

    def clean(self):
        with self.hosts.cd(project_dir):
            self.hosts.run('find . -name \'*.py?\' -exec rm -rf {} \;')

class Git(Node):
    project_directory = required_property()
    repository = required_property()

    def install(self):
        self.hosts.sudo('apt-get install git')

    def clone(self):
        with self.hosts.cd(self.project_directory, expand=True):
            self.hosts.run("git clone '%s'" % esc1(self.repository))

    def pull(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                try:
                    self.hosts.run("git pull")
                except ActionException:
                    self.stash()
                    self.pull()
    def stash(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                self.hosts.run("git stash")

    def checkout(self, commit):
        with self.hosts.cd(project_dir, expand=True):
            self.hosts.run("git checkout '%s'" % esc1(commit))

    def tag(self):
        with self.hosts.cd(project_dir, expand=True):
            self.hosts.run("git tag LIVE")
            self.hosts.run('export TAG="date +DEPLOYED-%F/%H%M"')
            self.hosts.run("git tag $TAG")
            self.hosts.run("git push origin LIVE $TAG")

class DjangoDeployment(Node):
    class virtual_env(VirtualEnv):
        location = home + virtualenv
        packages = []
        requirements_files = [project_dir + 'requirements.txt' ]

    class git(Git):
        project_directory = home + virtualenv
        repository = repo

    def setup(self):
        #self.git.checkout('release')
        self.virtual_env.clean()
        self.git.pull()
        self.hosts.run('export DJANGO_SETTINGS_MODULE=bookingsystem.production')
        self.virtual_env.setup_env()
        self.virtual_env.update_database()
        self.virtual_env.collectstatic()
        self.virtual_env.run_uwsgi()

    def run_cmd(self,cmd):
        self.hosts.run(cmd)

    def checkIfCJexists(self):
        self.hosts.run('crontab -l')

    def addCJ(self):
        backup = '0 0 * * * main ' + project_dir + ' manage.py dbbackup > ' + cronLog
        checkIfRunning = '@hourly ' + project_dir + ' manage.py checkIfRunning > ' + cronLog
        removeStaleBookings = '0 0 * * * ' + project_dir + ' manage.py deleteStaleBk > ' + cronLog
        runOnBoot = '@reboot ' + project_dir + 'runOnBoot.sh'
        backup = '{ crontab -l -u main; echo "'+ backup +'"; } | crontab -u main -'
        checkIfRunning = '{ crontab -l -u main; echo "'+ checkIfRunning +'"; } | crontab -u main -'
        removeStaleBookings = '{ crontab -l -u main; echo "'+ removeStaleBookings +'"; } | crontab -u main -'
        runOnBoot = '{ crontab -l -u main; echo "'+ runOnBoot +'"; } | crontab -u main -'
        self.hosts.run(removeStaleBookings)
        self.hosts.run(backup)
        self.hosts.run(checkIfRunning)
        self.hosts.run(runOnBoot)
    
    def fullSetup(self):
        #self.hosts.sudo('apt-get update && apt-get install mysql-client-5.7 build-essential libssl-dev libffi-dev virtualenv uwsgi nginx libmysqlclient-dev python-pip')
        #self.hosts.sudo('virtualenv ' + virtualenv)
        #self.git.clone()
        #self.virtual_env.setup_env()
        #self.remove_defaultconf()
        #self.copy_nginx_conf()
        #self.restart_nginx()
        try:
            self.checkIfCJexists()
        except ActionException:
            self.addCJ()
        #self.setup_emperor()
        

    def load_django_settings(self):
        self.hosts.run('export DJANGO_SETTINGS_MODULE=bookingsystem.production')

    def remove_defaultconf(self):
        self.hosts.sudo('rm /etc/nginx/sites-enabled/default')

    def copy_nginx_conf(self):
        self.hosts.sudo('ln -f -s ' + project_dir + 'config/bksys.conf /etc/nginx/sites-enabled/')

    def restart_nginx(self):
        self.hosts.sudo('/etc/init.d/nginx restart')

    def setup_emperor(self):
        self.create_dir('/etc/uwsgi')
        self.create_dir('/etc/uwsgi/vassals')
        self.copyConfig()
        self.start()

    def set_autowakeup(self):
        self.hosts.sudo('ln -f -s ' + project_dir + 'config/rc.local  /etc/rc.local')

    def create_dir(self,cmd):
        self.hosts.sudo('mkdir ' + cmd)

    def start(self):
        self.hosts.run('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')

    def copyConfig(self):
        self.hosts.sudo('ln -f -s ' + project_dir + 'start_app.ini /etc/uwsgi/vassals/')

class remote_host(SSHHost):
    address = ip 
    username = 'main'       
    key_filename = keyLocation    

class DjangoDeploymentOnHost(DjangoDeployment):
    class Hosts:
        host = remote_host

if __name__ == '__main__':
    start(DjangoDeploymentOnHost)