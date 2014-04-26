QuantCluster Command Line Interface (CLI)

QuantCluster is an open source cluster-computing toolkit for Amazon’s Elastic Compute Cloud (EC2). It is designed to provide a reproducible enviroment for quantitiative finance research that can be scaled to accomodate large problem sizes.

A number of open source tools are utilized:

    StarCluster - Cluster-computing toolkit for Amazon’s Elastic Compute Cloud
    OpenMPI - Library used for writing/running parallel applications
    Open Grid Scheduler - Queuing system for scheduling jobs on the cluster and handling load balancing.
    NFS - Network File System for sharing folders across the cluster.
    ATLAS - Automatically Tuned Linear Algebra Subroutines (custom built for larger EC2 instance types)
    IPython - An advanced interactive shell for Python. Notebooks provide a front end to the cluster.
    Numpy - Fast array and numerical library for Python (compiled against custom Atlas)
    Scipy - Scientific algorithms library for Python (compiled against custom Atlas)
    Numpy - Fast array and numerical library for Python (compiled against custom Atlas)
    Celery - Distributed task queue for upkeep
    Hadoop - Framework for writing massively distributed map/reduce tasks
    Hive - Data warehouse querying and managing large datasets residing in distributed storage

If you have Python and pip, you can install the QuantCluster Command Line Interface (CLI) with

    pip install git+git://github.com/quantcluster/quantcluster.git
    cd quantcluster/
    python setup.py install

Check that it is working:

    quantcluster listpublic


