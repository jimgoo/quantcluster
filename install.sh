#!/bin/bash

#sudo pip install StarCluster

QC_HOME=/mnt/quantcluster
cd $QC_HOME
# git clone https://github.com/quantcluster/quantcluster.git
# python setup.py develop
starcluster listpublic
rm -rf ~/.starcluster/config
rm -rf ~/.starcluster/plugins
ln -s /mnt/quantcluster/config ~/.starcluster/config
ln -s /mnt/quantcluster/quantcluster/plugins/ ~/.starcluster/plugins

## <TODO> Prompt user for AWS credentials, then save them to the SC config file
echo "Done"
