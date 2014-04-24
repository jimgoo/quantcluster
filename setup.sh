#!/bin/bash

sudo pip install StarCluster

# Get the CLI interface
git clone https://github.com/quantcluster/quantcluster.git

cd quantcluster/
python setup.py develop
cd ../

# remove old and link new
rm -rf ~/.starcluster/plugins
rm -rf ~/.starcluster/config
ln -s qc_cli/plugins ~/.starcluster/plugins
ln -s qc_cli/config ~/.starcluster/config

##
## <TODO> Prompt user for AWS credentials, then save them to the SC config file
##


