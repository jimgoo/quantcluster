
# BASE_AMI_ID = ami-3393a45a
# INSTANCE_TYPE = m3.xlarge
# starcluster start -o -s 1 -i $INSTANCE_TYPE -n $BASE_AMI_ID imagehost

starcluster start -o -s 1 -i m3.xlarge -n ami-3393a45a imagehost
starcluster listclusters --show-ssh-status imagehost
starcluster sshmaster imagehost
starcluster runplugin qc imagehost
starcluster ebsimage i-9c4777cf qc2

