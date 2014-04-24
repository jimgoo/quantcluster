# from starcluster import clustersetup
# from starcluster.logger import log

from starcluster.clustersetup import DefaultClusterSetup
from starcluster.logger import log
from starcluster.utils import print_timing

import datetime

'''
# Backup
cp /etc/exports /etc/exports_orig && cp /etc/fstab /etc/fstab_orig

# Restore
cp /etc/exports_orig /etc/exports && cp /etc/fstab_orig /etc/fstab
# <MASTER ONLY> exportfs -fra

# Display
more /etc/exports && echo "" && more /etc/fstab

'''
class RAID_10(DefaultClusterSetup):
    """

    Steps for adding RAID 10:

    - Mount the component drives r1-r8 via config file:

    # RAID 10 components
    [volume r1]
    VOLUME_ID = vol-xxxxxx
    MOUNT_PATH = /vols/r1
    ...
    [volume r8]
    VOLUME_ID = vol-xxxxxx
    MOUNT_PATH = /vols/r2

    # Cluster template that uses these RAID components
    [cluster testCluster]
p    VOLUMES = r1, r2, r3, r4, r5, r6, r7, r8
    ...
    
    - Create the /md0 array if it doesn't already exist (check that the names are the same!)
    
         sudo mdadm -v --create /dev/md0 --level=raid10 --raid-devices=8 /dev/xvdz /dev/xvdy /dev/xvdx /dev/xvdw /dev/xvdv /dev/xvdu /dev/xvdt /dev/xvds

          mdadm --assemble /dev/md0 /dev/xvdz /dev/xvdy /dev/xvdx /dev/xvdw /dev/xvdv /dev/xvdu /dev/xvdt /dev/xvds

    - Mount the RAID device on master node:

         mkdir /vols/raid10
         mount /dev/md0p1 /vols/raid10
    
    - On master node, add entries to /etc/exports for /vols/raid10 and remove entries for the raid components

    - Issue command to export master filesystem:
   
         exportfs -fra

    - For each non-master node, add an entry to /etc/fstab like this:
    
         master:/vols/raid /vols/raid nfs vers=3,user,rw,exec,noauto 0 0

         
    """
    def __init__(self):
        super(RAID_10, self).__init__()

    def run(self, nodes, master, user, user_shell, volumes):
    
        # Add mount point to NFS share
        #log.info("----> Adding RAID to NFS share")

        sNow = str(datetime.datetime.now())[0:10]
        
        if nodes:

            log.info("Installing package: mdadm")
            master.apt_install("mdadm")

            log.info("Assembling /dev/md0 RAID10 array")
            master.ssh.execute("mdadm --assemble /dev/md0 /dev/xvdz /dev/xvdy /dev/xvdx /dev/xvdw /dev/xvdv /dev/xvdu /dev/xvdt /dev/xvds")

            log.info("Creating mount point for RAID drive")
            master.ssh.execute("mkdir /vols/raid10")

            log.info("Mounting RAID drive")
            master.ssh.execute("mount /dev/md0p1 /vols/raid10")

            log.info("Updating /etc/exports for RAID drive")
            
            # Save a backup (/etc/exports_backup_yyyy-mm-dd
            master.ssh.execute('cp /etc/exports ' + '/etc/exports_backup_' + sNow)

            # Remove the RAID components r1-r8 from /etc/exports
            for i in range(8):
                regex = '/vols/r' + str(i+1) + " node"
                master.ssh.remove_lines_from_file('/etc/exports', regex)
            
            etc_exports = master.ssh.remote_file('/etc/exports', 'r')
            contents = etc_exports.read()
            etc_exports.close()

            # Add new entry in /etc/exports for the RAID mount point on master ONLY
            etc_exports = master.ssh.remote_file('/etc/exports', 'a')

            export_paths = ['/vols/raid10']
            nfs_export_settings = "(async,no_root_squash,no_subtree_check,rw)"
            
            for node in nodes:
                for path in export_paths:
                    export_line = ' '.join(
                        [path, node.alias + nfs_export_settings + '\n'])
                    if export_line not in contents and node.alias != master.alias:
                        etc_exports.write(export_line)
            etc_exports.close()

            # Tell NFS to update file sharing
            master.ssh.execute('exportfs -fra')

            log.info("Updating /etc/fstab for RAID drive")
            
            path = export_paths[0]
            
            # Update /etc/fstab of every node
            for node in nodes:

                # Save a backup (/etc/fstab_backup-yyyy-mm-dd)
                node.ssh.execute('cp /etc/fstab ' + '/etc/fstab_backup_' + sNow)

                # get the contents
                fstab = node.ssh.remote_file('/etc/fstab', 'r')
                contents = fstab.read()
                fstab.close()

                # open again for appending
                fstab = node.ssh.remote_file('/etc/fstab', 'a')

                if node.alias == master.alias:
                    #fstab_line = '%s %s nfs vers=3,user,rw,exec,noauto 0 0\n' % (path, path)
                    #<TODO> make entry for RAID device in fstab of master node
                    continue
                else:
                    fstab_line = '%s:%s %s nfs vers=3,user,rw,exec,noauto 0 0\n' % (master.alias, path, path) 

                if fstab_line not in contents:
                    fstab.write(fstab_line)

                fstab.close()

                if not node.ssh.path_exists(path):
                    node.ssh.makedirs(path)
                    
                node.ssh.execute('mount %s' % path)

            # log.info("----> Exporting FS to Nodes")
            # master.export_fs_to_nodes(nodes, export_paths)

            # log.info("----> Mounting NFS shares")
            # for node in nodes:
            #    node.mount_nfs_shares(master, export_paths)
                
        else:
            log.info("----> There are no nodes to NFS share with.")

        # self._nodes = nodes
        # self._master = master
        # self._user = user
        # self._user_shell = user_shell
        # self._volumes = volumes
                
    #def _setup_ebs_volumes(self):
        # """
        # Mount EBS volumes, if specified in ~/.starcluster/config to /home
        # """

        # print "====================================================================="
        # print " _setup_ebs_volumes"
        # print "====================================================================="
        
        #  # <JG>
        # log.info("Mounting RAID 10: mount " +  my_volume_partition + " " + my_mount_path)
        # self._master.mount_device(my_volume_partition, my_mount_path)
        
        # # setup /etc/fstab on master to use block device if specified
    #     master = self._master
    #     devs = master.ssh.ls('/dev')
    #     for vol in self._volumes:
    #         vol = self._volumes[vol]
    #         vol_id = vol.get("volume_id")
    #         mount_path = vol.get('mount_path')
    #         device = vol.get("device")
    #         volume_partition = vol.get('partition')
    #         if not (vol_id and device and mount_path):
    #             log.error("missing required settings for vol %s" % vol)
    #             continue
    #         dev_exists = master.ssh.path_exists(device)
    #         if not dev_exists and device.startswith('/dev/sd'):
    #             # check for "correct" device in unpatched kernels
    #             device = device.replace('/dev/sd', '/dev/xvd')
    #             dev_exists = master.ssh.path_exists(device)
    #         if not dev_exists:
    #             log.warn("Cannot find device %s for volume %s" %
    #                      (device, vol_id))
    #             log.warn("Not mounting %s on %s" % (vol_id, mount_path))
    #             log.warn("This usually means there was a problem "
    #                      "attaching the EBS volume to the master node")
    #             continue
    #         if not volume_partition:
    #             partitions = filter(lambda x: x.startswith(device), devs)
    #             if len(partitions) == 1:
    #                 volume_partition = device
    #             elif len(partitions) == 2:
    #                 volume_partition = device + '1'
    #             else:
    #                 log.error(
    #                     "volume has more than one partition, please specify "
    #                     "which partition to use (e.g. partition=0, "
    #                     "partition=1, etc.) in the volume's config")
    #                 continue
    #         elif not master.ssh.path_exists(volume_partition):
    #             log.warn("Cannot find partition %s on volume %s" %
    #                      (volume_partition, vol_id))
    #             log.warn("Not mounting %s on %s" % (vol_id,
    #                                                 mount_path))
    #             log.warn("This either means that the volume has not "
    #                      "been partitioned or that the partition"
    #                      "specified does not exist on the volume")
    #             continue
    #         log.info("Mounting EBS volume %s on %s..." % (vol_id, mount_path))
    #         mount_map = self._master.get_mount_map()
    #         dev = mount_map.get(volume_partition)
    #         if dev:
    #             path, fstype, options = dev
    #             if path != mount_path:
    #                 log.error("Volume %s is mounted on %s, not on %s" %
    #                           (vol_id, path, mount_path))
    #             else:
    #                 log.info(
    #                     "Volume %s already mounted on %s...skipping" %
    #                     (vol_id, mount_path))
    #             continue
    #         self._master.mount_device(volume_partition, mount_path)

    #     # <JG>
    #     log.info("Mounting RAID 10: mount " +  my_volume_partition + " " + my_mount_path)
    #     self._master.mount_device(my_volume_partition, my_mount_path)

    # # def _mount_nfs_shares(self, nodes, export_paths=None):
    # #     export_paths.append(my_mount_path)

        
    # def _get_nfs_export_paths(self):
    #     print "====================================================================="
    #     print " _get_nfs_export_paths"
    #     print "====================================================================="
        
    #     export_paths = ['/home', my_mount_path] # <JG> modded this line
    #     for vol in self._volumes:
    #         vol = self._volumes[vol]
    #         mount_path = vol.get('mount_path')
    #         if not mount_path in export_paths:
    #             export_paths.append(mount_path)

    #     log.info("Added new mount path: " + my_mount_path)
    #     print export_paths
                
    #     return export_paths
        
    ##
    ## Adding and removing nodes should auto-share via NFS...
    ##
        
    # def on_add_node(self, new_node, nodes, master, user, user_shell, volumes):
    #     raise NotImplementedError("on_remove_node method not implemented")
    
    # def on_remove_node(self, node, nodes, master, user, user_shell, volumes):
    #     raise NotImplementedError("on_remove_node method not implemented")
