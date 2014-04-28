
import sys

from setuptools import setup, find_packages

setup(
    name='quantcluster',
    url='http://www.quantcluster.com',
    version='0.0.1',
    description='A command line interface for QF cluster-computing on AWS EC2.',
    author='Jimmie Goode',
    author_email='jimmie@quantcluster.com',
    packages=find_packages(),
    install_requires=['StarCluster'],
    )
