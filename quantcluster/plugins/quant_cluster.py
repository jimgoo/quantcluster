import posixpath

from starcluster import clustersetup
from starcluster import threadpool
from starcluster.logger import log

# command for install git packages
git_cmd = """
mkdir %(PKG_DIR)s
cd %(PKG_DIR)s
git clone https://github.com/%(USER)s/%(PKG)s.git
cd %(PKG)s
sudo python setup.py develop
"""

class QuantCluster(clustersetup.ClusterSetup):
    
    def __init__(self, apt_pkgs='', pip_pkgs='', git_pkgs='', install_dir='/opt', install_tws=False):
        self.install_dir = install_dir
        self.apt_pkgs = [str(x).strip() for x in apt_pkgs.split(',') if x is not '']
        self.pip_pkgs = [str(x).strip() for x in pip_pkgs.split(',') if x is not '']
        self.git_pkgs = [str(x).strip() for x in git_pkgs.split(',') if x is not '']
        self.install_tws = install_tws
        self._pool = None

    @property
    def pool(self):
        if self._pool is None:
            self._pool = threadpool.get_thread_pool(20, disable_threads=False)
        return self._pool

    def apt_install(self, node):
        # Upgrade old packages - sudo apt-get update && 
        cmd = 'sudo apt-get install -y %s ' % ' '.join(self.apt_pkgs)
        log.info('%s>> %s' % (node.alias, cmd))
        node.ssh.execute(cmd)

    def pip_install(self, node):
        # Update old packages (-U)
        cmd = 'sudo pip install -U %s ' % ' '.join(self.pip_pkgs)
        log.info('%s>> %s' % (node.alias, cmd))
        node.ssh.execute(cmd)

    def git_install(self, node):
        for pkg in self.git_pkgs:
            assert pkg != ''
            toks = pkg.split('/')
            git_user = toks[0]
            git_pkg = toks[1]
            
            cmd = git_cmd % {'USER': git_user,
                             'PKG': git_pkg,
                             'HOME': self.install_dir,
                             'PKG_DIR': posixpath.join(self.install_dir, git_pkg)}

            #cmd = 'sudo pip install git+https://github.com/%s/%s.git' % (git_user, git_pkg)
            log.info('%s>> %s' % (node.alias, cmd))    
            node.ssh.execute(cmd)

    def tws_install(self, node):
        cmd = "python -c 'from pulley.brokers.ib import tws; tws.install()'"
        log.info('%s>> %s' % (node.alias, cmd))
        node.ssh.execute(cmd)
        
    def run(self, nodes, master, user, user_shell, volumes):
        # order is important, apt pkgs should go first
        for node in nodes:
            self.pool.simple_job(self.apt_install, (node,), jobid=node.alias)
        self.pool.wait()
        for node in nodes:
            self.pool.simple_job(self.pip_install, (node,), jobid=node.alias)
        self.pool.wait()
        for node in nodes:
            self.pool.simple_job(self.git_install, (node,), jobid=node.alias)
        self.pool.wait()

        # install TWS on master node
        #if self.install_tws:
        #   self.tws_install(master)

        
