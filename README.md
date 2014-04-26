<h2>QuantCluster Command Line Interface (CLI)</h2>


<p>QuantCluster is an open source cluster-computing toolkit for Amazon’s Elastic Compute Cloud (EC2). It is designed to provide a reproducible environment for quantitative finance research that can be scaled to accommodate large problem sizes. This includes large numbers of time periods, large numbers of assets, and combinations thereof.
<p>A number of open source tools are utilized:</p>

<ul>
<li><a target="_blank" href="http://star.mit.edu/cluster/"><strong>StarCluster</strong></a> - Cluster-computing toolkit for Amazon&rsquo;s Elastic Compute Cloud</li>
<li><a target="_blank" href="http://www.open-mpi.org/"><strong>OpenMPI</strong></a> - Library used for writing/running parallel applications</li>
<li><a target="_blank" href="http://gridscheduler.sourceforge.net/"><strong>Open Grid Scheduler</strong></a> - Queuing system for scheduling jobs on the cluster and handling load balancing.</li>
<li><a href="http://en.wikipedia.org/wiki/Network_File_System"><strong>NFS</strong></a> - Network File System for sharing folders across the cluster.</li>
<li><a href="http://math-atlas.sourceforge.net/"><strong>ATLAS</strong></a> - Automatically Tuned Linear Algebra Subroutines (custom built for larger EC2 instance types)</li>
<li><a target="_parent" href="http://ipython.org/"><strong></strong></a><a target="_parent" href="http://ipython.org/"><strong>IPython</strong></a> - An advanced interactive shell for Python. Notebooks provide a front end to the cluster.</li>
<li><a target="_blank" href="http://www.numpy.org/"><strong>Numpy</strong></a> - Fast array and numerical library for Python (compiled against custom Atlas)</li>
<li><a href="http://www.scipy.org/"><strong>Scipy</strong></a> - Scientific algorithms library for Python (compiled against custom Atlas)</li>
<li><a target="_blank" href="http://www.numpy.org/"><strong>Numpy</strong></a> - Fast array and numerical library for Python (compiled against custom Atlas)</li>
<li><a target="_blank" href="https://pypi.python.org/pypi/django-celery"><strong>Celery </strong></a>- Distributed task queue for upkeep<strong></strong></li>
<li><a target="_blank" href="http://hadoop.apache.org/"><strong>Hadoop</strong></a> - Framework for writing massively distributed map/reduce tasks</li>
<li><strong><a href="http://hive.apache.org/">Hive</a> </strong>- Data warehouse querying and managing large datasets residing in distributed storage</li>
</ul>
<p>If you have Python and pip, you can install the QuantCluster CLI with:</p>
<pre class="lang-py prettyprint prettyprinted">
<code>pip install git+git://github.com/quantcluster/quantcluster.git
cd quantcluster
python setup.py install<br />
</code></pre>
<p>Check that everything is working by listing all Amazon EC2 public images that can be spun up as a cluster</p>
<pre class="lang-py prettyprint prettyprinted"><code>quantcluster listpublic</code></pre>
