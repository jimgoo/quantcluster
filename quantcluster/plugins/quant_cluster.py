import posixpath

from starcluster import clustersetup
from starcluster import threadpool
from starcluster.logger import log

INSTALL_DIR = '/opt'

class QuantCluster(clustersetup.ClusterSetup):
    
    def __init__(self):
        self._pool = None
        self.apt_pkgs = ['libpq-dev', 'postgresql', 'postgresql-client']
        self.pip_pkgs = ['swigibpy', 'six', 'scikit-learn'] # celery[librabbitmq]
        self.git_pkgs = ['jgoode21/lakehouse', 'jgoode21/zipline']
        
    @property
    def pool(self):
        if self._pool is None:
            self._pool = threadpool.get_thread_pool(20, disable_threads=False)
        return self._pool

    def apt_install(self, node):
        cmd = 'sudo apt-get install -y %s ' % (' '.join(self.apt_pkgs))
        log.info('%s> %s' % (node.alias, cmd))
        node.ssh.execute(cmd)        

    def pip_install(self, node):
        cmd = 'sudo pip install %s ' % (' '.join(self.pip_pkgs))
        log.info('%s> %s' % (node.alias, cmd))
        node.ssh.execute(cmd)

    def git_install(self, node):
        cmd = ''
        for pkg in self.git_pkgs:
            cmd += 'cd %(INSTALL_DIR)s\ngit clone https://github.com/%(PKG)s.git\ncd %(PKG)s\nsudo python setup.py develop \n' % \
                   {'PKG': pkg, 'INSTALL_DIR': INSTALL_DIR}
            
        log.info('%s> %s' % (node.alias, cmd))
        node.ssh.execute(cmd)
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            self.pool.simple_job(self.apt_install, (node,), jobid=node.alias)
        self.pool.wait()
        for node in nodes:
            self.pool.simple_job(self.pip_install, (node,), jobid=node.alias)
        self.pool.wait()
        for node in nodes:
            self.pool.simple_job(self.git_install, (node,), jobid=node.alias)
        self.pool.wait()
