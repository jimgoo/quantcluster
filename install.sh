#!/bin/bash


#sudo pip install StarCluster

QC_HOME=/opt
cd $QC_HOME
git clone https://github.com/quantcluster/quantcluster.git
cd quantcluster/
python setup.py develop
starcluster listpublic
# >> enter 'q' at prompt

# remove old and link new
ln -s $QC_HOME/quantcluster/quantcluster/config ~/.starcluster/config
ln -s $QC_HOME/quantcluster/quantcluster/plugins ~/.starcluster/plugins


## <TODO> Prompt user for AWS credentials, then save them to the SC config file

echo "Done"