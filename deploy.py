#!/usr/bin/env python
from deployer.client import start
from deployer.node import Node, required_property
from deployer.utils import esc1
from deployer.host import SSHHost
from deployer.exceptions import ActionException

home = '/home/main/'
ip = '51.140.55.58'
project_name = "bookingsystem/"
virtualenv = "BKSYSDEPLOY/"
project_dir = home + virtualenv + project_name
repo = 'https://github.com/nijaaam/bookingsystem.git'
keyLocation = '/home/jamun-g/Desktop/keys/bookingsystem'


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
                self.hosts.run("git pull")
    
    def stash(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                self.hosts.run("git stash")

    def checkout(self, commit):
        with self.hosts.cd(project_dir, expand=True):
            self.hosts.run("git checkout '%s'" % esc1(commit))

class DjangoDeployment(Node):
    class virtual_env(VirtualEnv):
        location = home + virtualenv
        packages = []
        requirements_files = [project_dir + 'requirements.txt' ]

    class git(Git):
        project_directory = home + virtualenv
        repository = repo

    def setup(self):
        self.git.pull()
        self.virtual_env.setup_env()
        self.virtual_env.update_database()
        self.virtual_env.collectstatic()
        self.virtual_env.run_uwsgi()

    def fullSetup(self):
        self.hosts.sudo('apt-get update && apt-get install virtualenv uwsgi nginx libmysqlclient-dev python-pip')
        self.hosts.run('virtualenv' + virtualenv)
        self.git.clone()
        self.virtual_env.setup_env()
        self.remove_defaultconf()
        self.copy_nginx_conf()
        self.restart_nginx()
        self.setup_emperor()

    def upload_django_settings(self):
        with self.hosts.open('~/BKSYSDEPLOY/local_settings.py') as f:
            f.write(django_settings)

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