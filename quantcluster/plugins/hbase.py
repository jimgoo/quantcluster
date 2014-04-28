import posixpath
import traceback

from starcluster import threadpool
from starcluster.logger import log

from starcluster import clustersetup

hbase_site_templ = """\
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://master:54310/hbase</value>
    <description>The directory shared by RegionServers.
    </description>
  </property>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
    <description>The mode the cluster will be in. Possible values are                      
    false: standalone and pseudo-distributed setups with managed Zookeeper                  
    true: fully-distributed with unmanaged Zookeeper Quorum (see hbase-env.sh)
    </description>
  </property>
</configuration>
"""

HBASE_VER = "0.94.8"
HBASE_NAME = "hbase-" + HBASE_VER
HBASE_TAR = HBASE_NAME + ".tar.gz"
HBASE_URL = "https://s3.amazonaws.com/cladogenesis_downloads/" + HBASE_TAR

class Hbase(clustersetup.ClusterSetup):

    def __init__(self,
                 hadoop_home='/usr/lib/hadoop-0.20/',
                 hadoop_core='/usr/lib/hadoop-0.20/hadoop-core-0.20.2-cdh3u5.jar'):
        self.hadoop_home = hadoop_home
        self.hadoop_core = hadoop_core
        self.hbase_conf = '/opt/hbase/conf'
        self.centos_java_home = '/usr/lib/jvm/java'
        self.ubuntu_javas = ['/usr/lib/jvm/default-java/jre']
        self._pool = None

    @property
    def pool(self):
        if self._pool is None:
            self._pool = threadpool.get_thread_pool(20, disable_threads=False)
        return self._pool

    def _get_java_home(self, node):
        # check for CentOS, otherwise default to Ubuntu 10.04's JAVA_HOME
        if node.ssh.isfile('/etc/redhat-release'):
            return self.centos_java_home
        for java in self.ubuntu_javas:
            if node.ssh.isdir(java):
                return java
        raise Exception("Cant find JAVA jre")

    def _has_tar(self, node):
        if node.ssh.isfile("/opt/" + HBASE_TAR):
            return True
        else:
            return False
    
    def _download(self, node):
        if self._has_tar(node):
            log.info("TAR file already present, skipping download")
            return
        cmd = "cd /opt && curl -O " + HBASE_URL               
        log.info("Downloading tar on  " + node.alias + " with: " + HBASE_URL)
        node.ssh.execute(cmd)
        log.info("Downloaded tarball OK.")

    def _extract(self, master, node):
        # remove old symlinked install 
        if node.ssh.isdir('/opt/hbase'):
            node.ssh.execute("rm -rf /opt/hbase")

        # remove previous extraction
        if node.ssh.isdir('/opt/' + HBASE_NAME):
            node.ssh.execute("rm -rf /opt/" + HBASE_NAME)
            
        # transfer tar from master node (b/c using curl on 100s of nodes might overload the host)
        #if node.alias != master.alias and self._has_tar(node) == False:
        #    master.ssh.execute("scp /opt/" + HBASE_TAR + " " + node.alias + ":/opt/")

        self._download(node)
            
        # extract and symlink
        node.ssh.execute("cd /opt && " +
                         "tar -zxf " + HBASE_TAR + " && " +
                         "ln -s " + HBASE_NAME + " hbase")

    def _configure_hbase_site(self, node):
        fname = posixpath.join(self.hbase_conf, 'hbase-site.xml')
        f = node.ssh.remote_file(fname)
        f.write(hbase_site_templ)
        f.close()
        
    def _configure_env(self, node):
        fname = posixpath.join(self.hbase_conf, 'hbase-env.sh')
        node.ssh.remove_lines_from_file(fname, 'JAVA_HOME')
        f = node.ssh.remote_file(fname, 'a')
        f.write('export JAVA_HOME=%s\n' % self._get_java_home(node))
        f.close()

    def _configure_regionservers(self, node, node_aliases):
        fname = posixpath.join(self.hbase_conf, 'regionservers')
        f = node.ssh.remote_file(fname)
        f.write('\n'.join(node_aliases))
        f.close()
        
    def _configure_all(self, master, nodes, user):
        
        node_aliases = map(lambda n: n.alias, nodes)

        log.info("Getting tarball on master...")
        self._download(master)
        
        log.info("Distributing and extracting tarball on nodes...")
        for node in nodes:
            self.pool.simple_job(self._extract, (master,node),
                               jobid=node.alias)
        self.pool.wait(numtasks=len(nodes))

        log.info("Configuring conf/hbase-site.xml...")
        for node in nodes:
            self.pool.simple_job(self._configure_hbase_site, (node,),
                                 jobid=node.alias)
        self.pool.wait(numtasks=len(nodes))

        log.info("Configuring conf/hbase-env.sh...")
        for node in nodes:
            self.pool.simple_job(self._configure_env, (node,),
                                 jobid=node.alias)
        self.pool.wait(numtasks=len(nodes))

        log.info("Configuring conf/regionservers...")
        for node in nodes:
            self.pool.simple_job(self._configure_regionservers, (node,node_aliases),
                                 jobid=node.alias)
        self.pool.wait(numtasks=len(nodes))

    def _start_all(self, master, nodes):
       
        # Copy hadoop-core jar into the hbase/lib/ directory
        for node in nodes:
            node.ssh.execute("cp %s /opt/hbase/lib/" % self.hadoop_core)
            
            # node.ssh.execute("rm -f /opt/hbase/lib/hadoop-core-*.jar && " +
            #                  "cp /opt/hadoop/hadoop-core-*.jar /opt/hbase/lib/")
        
        # Permanently add 'localhost' to the list of known hosts.
        master.ssh.execute("ssh-keyscan localhost 2>&1 | sort -u - ~/.ssh/known_hosts > ~/.ssh/tmp_hosts")
        master.ssh.execute("cat ~/.ssh/tmp_hosts >> ~/.ssh/known_hosts")

        
        # Raise limits on the number of open files
        # Raise limits on the number of user processes
        master.ssh.execute("ulimit -n 50000 && " +
                           "ulimit -u 500000 && " +
                           "cd /opt/hbase && " +
                           "bin/start-hbase.sh")

    def _open_ports(self, master):
        ports = [60010, 60030]
        ec2 = master.ec2
        for group in master.cluster_groups:
            for port in ports:
                has_perm = ec2.has_permission(group, 'tcp', port, port,
                                              '0.0.0.0/0')
                if not has_perm:
                    group.authorize('tcp', port, port, '0.0.0.0/0')
        
    def run(self, nodes, master, user, user_shell, volumes):

        self._configure_all(master, nodes, user)
        self._start_all(master, nodes)
        self._open_ports(master)

        log.info("HBase Monitor:                 http://%s:60010" % master.dns_name)
        log.info("HBase RegionServer at master:  http://%s:60030" % master.dns_name)
'''
hbase>>
create 'test', 'cf'
put 'test', 'row1', 'cf:a', 'value1'
scan 'test'
'''
