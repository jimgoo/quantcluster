<h1>QuantCluster</h1>
<p><span>QuantCluster is a set of plugins for MIT's&nbsp;</span><a href="http://star.mit.edu/cluster/">StarCluster</a><span>&nbsp;that have proven useful for quantitative finance research with Amazon&rsquo;s Elastic Compute Cloud (EC2).&nbsp; It provides reproducible parallel computing environments that can be scaled up to accommodate </span><span>large problem sizes.</span></p>
<h4><em>Python stack</em></h4>
<ul>
<li><a href="http://ipython.org/">IPython</a> - An advanced interactive shell for Python with notebooks.</li>
<li><a href="http://www.numpy.org/">NumPy</a> - Fast array and numerical library for Python (compiled against OpenBLAS).</li>
<li><a href="http://www.scipy.org/">SciPy</a> - Scientific algorithms library for Python (compiled against OpenBLAS).</li>
<li><a href="http://pandas.pydata.org/">Pandas</a> - Data analysis tools for Python.</li>
<li><a href="https://github.com/quantopian/zipline">Zipline</a> - Algorithmic trading library.</li>
<li><a href="https://github.com/Komnomnomnom/swigibpy">swigibpy</a> - Third party Interactive Brokers Python API generated from TWS C++ API using SWIG.</li>
<li><a href="http://www.celeryproject.org/">Celery </a>- Fault tolerant distributed task queue for live strategy execution and data processing.</li>
</ul>
<h4><em>Big data stack</em></h4>
<ul>
<li><a href="http://hadoop.apache.org/">Apache Hadoop</a> - Framework for writing massively distributed map/reduce tasks.</li>
<li><a href="http://hadoop.apache.org/">Apache Hive</a> - Data warehouse querying and managing large datasets residing in distributed storage.</li>
<li><a href="http://hadoop.apache.org/">Apache HBase</a> - Random, realtime read/write access to big financial data.</li>
</ul>
<h4><em>HPC Stack</em></h4>
<ul>
<li><a href="http://www.open-mpi.org/">OpenMPI</a> - Library used for writing/running parallel applications.</li>
<li><a href="http://openmp.org/">OpenMP</a> - Library for shared memory multiprocessing.</li>
<li><a href="http://www.openblas.net/">OpenBLAS</a> - Multi-threaded BLAS library.</li>
<li><a href="http://gridscheduler.sourceforge.net/">Open Grid Scheduler</a> - Queuing system for scheduling jobs on the cluster and handling load balancing.</li>
<li><a href="http://en.wikipedia.org/wiki/Network_File_System">NFS</a> - Network File System for sharing folders across the cluster.</li>
</ul>


<h3>Install with pip</h3>
<pre><code>pip install quantcluster</code></pre>

More info at <a href="http://goodeanalytics.com/clusters/ec2-clusters/">GoodeAnalytics.com</a>.

Documentation at <a href="http://star.mit.edu/cluster/docs/latest/">StarCluster site</a>.
