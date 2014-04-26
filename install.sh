#!/bin/bash

sudo pip install 

# Get the CLI interface
git clone https://github.com/quantcluster/quantcluster.git

cd quantcluster/
python setup.py develop
cd ../

# remove old and link new
rm -rf ~/.starcluster/plugins
rm -rf ~/.starcluster/config
ln -s quantcluster/plugins ~/.starcluster/plugins
ln -s quantcluster/config ~/.starcluster/config

## <TODO> Prompt user for AWS credentials, then save them to the SC config file
