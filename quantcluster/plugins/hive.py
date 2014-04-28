import posixpath

from starcluster.clustersetup import DefaultClusterSetup
from starcluster.logger import log
from starcluster.utils import print_timing

VER = "0.10.0"
NAME = "hive-" + VER
TAR = NAME + ".tar.gz"
URL = "https://s3.amazonaws.com/cladogenesis_downloads/" + TAR

class Hive(DefaultClusterSetup):
    
    def __init__(self):
        super(Hive, self).__init__()

    def _has_tar(self, node):
        if node.ssh.isfile("/opt/" + TAR):
            return True
        else:
            return False
        
    def _download(self, master):

        if self._has_tar(master):
            log.info("TAR file already on master, skipping download.")
            return
        
        cmd = "cd /opt && curl -O " + URL
        
        log.info("Downloading tar on MASTER with: " + URL)
        master.ssh.execute(cmd)
        log.info("Downloaded tarball OK.")
        
    def _extract(self, node):

        # remove old symlink to install 
        if node.ssh.isdir('/opt/hive'):
            node.ssh.execute("rm -rf /opt/hive")

        # remove previous extraction
        if node.ssh.isdir('/opt/' + NAME):
            node.ssh.execute("rm -rf /opt/" + NAME)

        # extract and symlink
        node.ssh.execute("cd /opt && " +
                         "tar -zxf " + TAR + " && " +
                         "ln -s " + NAME + " hive")


    def _add_path(self, node):
        env_file = node.ssh.remote_file('/etc/profile', 'a')
        env_file.write('export PATH=$PATH:/opt/hive/bin \n')
        env_file.close()
        
    def run(self, nodes, master, user, user_shell, volumes):

        log.info("Installing files...")
        self._download(master)
        self._extract(master)
        self._add_path(master)
        
        log.info("Configuring HDFS directories for Hive...")
        master.ssh.execute("hadoop fs -mkdir /tmp && " +
                           "hadoop fs -mkdir /user/hive/warehouse && " +
                           "hadoop fs -chmod g+w /tmp && " + 
                           "hadoop fs -chmod g+w /user/hive/warehouse")

        # <TODO> To use bin/hive, you need to set this:
        # export HADOOP_HOME=/opt/hadoop

