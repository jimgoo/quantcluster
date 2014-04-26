import posixpath

from starcluster import threadpool
from starcluster import clustersetup
from starcluster.logger import log

class QuantCluster(clustersetup.ClusterSetup):
    """
    Configures Hadoop using Cloudera packages on StarCluster
    """
    def __init__(self):
        self._pool = None
        self.pip_pkgs = ['celery[librabbitmq]', 'swigibpy' 'scikit-learn' 'six']
        self.apt_pkgs = ['libpq-dev', 'postgresql' 'postgresql-client']

    @property
    def pool(self):
        if self._pool is None:
            self._pool = threadpool.get_thread_pool(20, disable_threads=False)
        return self._pool

    def apt_install(self, nodes):
        cmd = 'sudo apt-get install %s ' % (self.apt_pkgs.join(' '))
        log.info('----> QuantCluster>  %s' cmd)
        node.ssh.execute(cmd)        

    def pip_install(self, nodes):
        cmd = 'sudo pip install -U %s ' % (self.pip_pkgs.join(' '))
        log.info('----> QuantCluster>  %s' cmd)
        node.ssh.execute(cmd)
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            self.pool.simple_job(self.apt_install, (node,), jobid=node.alias)
        for node in nodes:
            self.pool.simple_job(self.pip_install, (node,), jobid=node.alias)            
            
