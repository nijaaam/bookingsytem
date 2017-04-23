#!/usr/bin/env python
from deployer.client import start
from deployer.node import Node, required_property
from deployer.utils import esc1
from deployer.host import SSHHost
from deployer.exceptions import ActionException

home = '/home/main/'
#ip = 'bkwebtesting2086.cloudapp.net'
ip = 'bkwebsiteproduction9834.cloudapp.net'
project_name = "bookingsystem/"
virtualenv = "BKSYSDEPLOY/"
project_dir = home + virtualenv + project_name
repo = 'https://github.com/nijaaam/bookingsystem.git'
keyLocation = '/home/jamun-g/Desktop/keys/bookingsystem'
cronLog = ' & >> /var/log/cronjobs.log'

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
                self.hosts.sudo('./manage.py %s' % command)

    def run_uwsgi(self):
        with self.hosts.prefix(self.activate_cmd):
            with self.hosts.cd(project_dir):
                self.hosts.sudo('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')

    def collectstatic(self):
        self.run_management_command('collectstatic --clear --noinput --settings=bookingsystem.production')

    def update_database(self):
        self.run_management_command('migrate --noinput --settings=bookingsystem.production')

    def clean(self):
        with self.hosts.cd(project_dir):
            self.hosts.sudo('find . -name \'*.py?\' -exec rm -rf {} \;')

class Git(Node):
    project_directory = required_property()
    repository = required_property()

    def install(self):
        self.hosts.sudo('apt-get install git')

    def clone(self):
        with self.hosts.cd(self.project_directory, expand=True):
            self.hosts.sudo("git clone '%s'" % esc1(self.repository))

    def pull(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                try:
                    self.hosts.sudo("git pull")
                except ActionException:
                    self.stash()
                    self.pull()
    def stash(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                self.hosts.run("git stash")

    def checkout(self, commit):
        with self.hosts.cd(project_dir, expand=True):
            self.hosts.sudo("git checkout '%s'" % esc1(commit))

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
        self.git.checkout('release')
        self.git.pull()
        self.virtual_env.setup_env()
        self.virtual_env.update_database()
        self.virtual_env.collectstatic()
        #self.git.tag()
        self.virtual_env.run_uwsgi()

    def checkIfCJexists(self):
        self.hosts.run('crontab -l')

    def addCJ(self):
        backup = '0 0 * * * main ' + project_dir + ' manage.py dbbackup  ' + cronLog
        checkIfRunning = '@hourly ' + project_dir + ' manage.py checkIfRunning ' + cronLog
        removeStaleBookings = '0 0 * * * ' + project_dir + ' manage.py deleteStaleBk ' + cronLog
        runOnBoot = '@reboot ' + project_dir + 'scripts/runOnBoot.sh'
        backup = '{ crontab -l -u main; echo "'+ backup +'"; } | crontab -u main -'
        checkIfRunning = '{ crontab -l -u main; echo "'+ checkIfRunning +'"; } | crontab -u main -'
        removeStaleBookings = '{ crontab -l -u main; echo "'+ removeStaleBookings +'"; } | crontab -u main -'
        runOnBoot = '{ crontab -l -u main; echo "'+ runOnBoot +'"; } | crontab -u main -'
        self.hosts.run(removeStaleBookings)
        self.hosts.run(backup)
        self.hosts.run(checkIfRunning)
        self.hosts.run(runOnBoot)
    
    def fullSetup(self):
        self.hosts.sudo('apt-get update && apt-get install mysql-client-5.7 build-essential libssl-dev libffi-dev virtualenv uwsgi nginx libmysqlclient-dev python-pip')
        self.hosts.sudo('virtualenv ' + virtualenv)
        self.setproductionsettings()
        try:
            self.git.clone()
        except ActionException:
            pass
        self.virtual_env.setup_env()
        self.runSpecialCmd('rm /etc/nginx/sites-enabled/default')
        self.hosts.sudo('ln -f -s ' + project_dir + 'config/bksys.conf /etc/nginx/sites-enabled/')
        self.hosts.sudo('/etc/init.d/nginx restart')
        try:
            self.checkIfCJexists()
        except ActionException:
            self.addCJ()
        self.runSpecialCmd('mkdir /etc/uwsgi')
        self.runSpecialCmd('mkdir /etc/uwsgi/vassals')
        self.hosts.sudo('ln -f -s ' + project_dir + 'scripts/start_app.ini /etc/uwsgi/vassals/')
        self.runSpecialCmd('mkdir /var/uwsgi')
        self.runSpecialCmd('chown www-data:www-data /var/uwsgi')
        self.runSpecialCmd('chown -R www-data:www-data BKSYSDEPLOY/')
        self.setup()
        #self.hosts.sudo('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')


    def runSpecialCmd(self,cmd):
        try:
            self.hosts.sudo(cmd)
        except:
            pass

    def setproductionsettings(self):
        self.hosts.sudo('touch /etc/production.txt')
        self.hosts.sudo("echo 'x3h)318k2awulf%&e@z08!tswh21&tbt!wdya4osy5o797l_7(' >> /etc/production.txt")
        self.hosts.sudo('echo "dbbackupbksys" >> /etc/production.txt')
        self.hosts.sudo('echo "CkD5/KNWSF/BV4sM0XcnyrfBgPmZXjQW4i/FR4l2wX2Mn/PMZtZ/5u9D2wP6JUpXHDyJUwDtaiAECnuOYBPmfw==" >> /etc/production.txt')
        self.hosts.sudo('echo "bksysdb" >> /etc/production.txt')

class remote_host(SSHHost):
    address = ip 
    username = 'main'       
    key_filename = keyLocation    

class DjangoDeploymentOnHost(DjangoDeployment):
    class Hosts:
        host = remote_host

if __name__ == '__main__':
    start(DjangoDeploymentOnHost)
