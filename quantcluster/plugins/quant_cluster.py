# import posixpath

from starcluster import clustersetup
from starcluster import threadpool
from starcluster.logger import log

git_cmd = """
rm -rf %(home)s
cd %(base)s
git clone https://github.com/%(user)s/%(pkg)s.git
cd %(pkg)s
sudo python setup.py develop
"""

class QuantCluster(clustersetup.ClusterSetup):
    
    def __init__(self, install_dir='/opt', apt_pkgs='', pip_pkgs='', git_pkgs=''):
        
        self.install_dir = install_dir
        self.apt_pkgs = [str(x).strip() for x in apt_pkgs.split(',') if x is not '']
        self.pip_pkgs = [str(x).strip() for x in pip_pkgs.split(',') if x is not '']
        self.git_pkgs = [str(x).strip() for x in git_pkgs.split(',') if x is not '']        
        
        self._pool = None
        self.apt_pkgs = []
        self.pip_pkgs = []

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
        for pkg in self.git_pkgs:
            assert pkg != ''
            toks = pkg.split('/')
            git_user = toks[0]
            git_pkg = toks[1]
            
            git_cmd_pkg = git_cmd % {'pkg': pkg,
                                     'user': git_user,
                                     'pkg': git_pkg,
                                     'base': self.install_dir,
                                     'home': self.install_dir + '/' + git_pkg}
            print git_cmd_pkg
            
            node.ssh.execute(git_cmd_pkg)
        
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            self.pool.simple_job(self.git_install, (node,), jobid=node.alias)
        self.pool.wait()
        for node in nodes:
            self.pool.simple_job(self.apt_install, (node,), jobid=node.alias)
        self.pool.wait()
        for node in nodes:
            self.pool.simple_job(self.pip_install, (node,), jobid=node.alias)
        self.pool.wait()
