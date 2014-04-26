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
rm -rf ~/.starcluster
mkdir ~/.starcluster
cp $QC_HOME/quantcluster/config ~/.starcluster/config
cp -r $QC_HOME/quantcluster/quantcluster/plugins ~/.starcluster/


## <TODO> Prompt user for AWS credentials, then save them to the SC config file

echo "Done"