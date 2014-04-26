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
        self.apt_pkgs = ['libpq-dev', 'postgresql' 'postgresql-client']
        self.pip_pkgs = ['celery[librabbitmq]', 'swigibpy' 'scikit-learn' 'six']
        self.git_pkgs = ['jgoode21/lakehouse', 'jgoode21/zipline']
        
    @property
    def pool(self):
        if self._pool is None:
            self._pool = threadpool.get_thread_pool(20, disable_threads=False)
        return self._pool

    def apt_install(self, node):
        cmd = 'sudo apt-get install -y %s ' % (' '.join(self.apt_pkgs))
        node.ssh.execute(cmd)        

    def pip_install(self, node):
        cmd = 'sudo pip install --upgrade %s ' % (' '.join(self.pip_pkgs))
        node.ssh.execute(cmd)

    def git_install(self, node):
        cmd = ''
        for pkg in self.git_pkjs:
            cmd += 'cd /mnt && git clone https://%s.git' % pkg
            node.ssh.execute(cmd)
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            self.pool.simple_job(self.apt_install, (node,), jobid=node.alias)
        for node in nodes:
            self.pool.simple_job(self.pip_install, (node,), jobid=node.alias)            
        for node in nodes:
            self.pool.simple_job(self.git_install, (node,), jobid=node.alias)            
