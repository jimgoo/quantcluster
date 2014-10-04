<h1>QuantCluster</h1>
<p><span>QuantCluster is a set of plugins for MIT's&nbsp;</span><a href="http://star.mit.edu/cluster/">StarCluster</a><span>&nbsp;that have useful for scalable quantitative finance research with Amazon&rsquo;s Elastic Compute Cloud (EC2).&nbsp; It provides reproducible parallel computing environments that can be scaled up to accommodate </span><span>large problem sizes.</span></p>
<p><span color="#000000"><span><span>Arbitrarily large clusters can be created and are pre-configured with the following:</span></span></span></p>
<ul>
<li><a href="http://hadoop.apache.org/">Apache Hadoop</a> - Framework for writing massively distributed map/reduce tasks.</li>
<li><a href="http://hive.apache.org/">Apache Hive</a> - Data warehouse querying and managing large datasets residing in distributed storage.</li>
<li><a href="http://hbase.apache.org/">Apache HBase</a> - Random, realtime read/write access to big financial data.</li>
<li><a href="https://github.com/quantopian/zipline">Zipline</a><span>&nbsp;- Algorithmic trading library.</span></li>
<li><a href="https://github.com/Komnomnomnom/swigibpy">swigibpy</a><span>&nbsp;- Third party Interactive Brokers Python API generated from TWS C++ API using SWIG.</span></li>
<li><a href="/clusters/pulley-library/">Pulley</a><span>&nbsp;- Library for automated trading execution linking above two.</span></li>
<li><a href="http://ipython.org/">IPython</a> - An advanced interactive shell for Python with notebooks.</li>
<li><a href="http://www.numpy.org/">NumPy</a> - Fast array and numerical library for Python (compiled against OpenBLAS).</li>
<li><a href="http://www.scipy.org/">SciPy</a> - Scientific algorithms library for Python (compiled against OpenBLAS).</li>
<li><a href="http://pandas.pydata.org/">Pandas</a> - Data analysis tools for Python.</li>
<li><a href="http://www.open-mpi.org/">OpenMPI</a> - Library used for writing/running parallel applications.</li>
<li><a href="http://openmp.org/">OpenMP</a> - Library for shared memory multiprocessing.</li>
<li><a href="http://www.openblas.net/">OpenBLAS</a> - Multi-threaded BLAS library.</li>
<li><a href="http://gridscheduler.sourceforge.net/">Open Grid Scheduler</a> - Queuing system for scheduling jobs on the cluster and handling load balancing.</li>
<li><a href="http://en.wikipedia.org/wiki/Network_File_System">NFS</a> - Network File System for sharing folders across the cluster.</li>
<li><a href="http://www.celeryproject.org/">Celery&nbsp;</a><span>- Fault tolerant distributed task queue for live strategy execution and data processing.</span></li>
</ul>

<h3>Install with pip</h3>
<pre><code>pip install quantcluster</code></pre>

More info at <a href="http://goodeanalytics.com/clusters/ec2-clusters/">GoodeAnalytics.com</a>.

Documentation at <a href="http://star.mit.edu/cluster/docs/latest/">StarCluster site</a>.
