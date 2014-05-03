import posixpath

from starcluster import clustersetup
from starcluster import threadpool
from starcluster.logger import log

home_tmpl = """\
{% load staticfiles %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE|default:"en-us" }}">
  <head>
	<title>{% block title %}{% endblock %}</title>
  </head>
<body>
  {% block navbar %}{% block extrabutt %}{% endblock %}{% endblock %}
  {% block precontainer %}{% endblock %}
  <div class="container-fluid">
     <div class="row-fluid">
      <div class="span12">
       {% block container %}
	{% block breadcrumbs %}{% endblock %}
	<h4>QuantCluster %(IP)s</h4>
        <ul>
	  <li>https://%(IP)s:8888 – IPython notebooks </li>
	  <li>http://%(IP)s:50030 – Hadoop Job Tracker</li>
	  <li>http://%(IP)s:50070 – Hadoop name node</li>
	  <li>http://%(IP)s:60010 – Hbase master</li>
	  <li>http://%(IP)s:60030 – Hbase region server</li>
        </ul>
	{% endblock %}
      </div>
   </div>
   <div class="footer">
      {% block footer %}
      {% endblock %}
   </div>
 </div>
  {% block postcontainer %}{% endblock %}
</body>
{% block postbody %}{% endblock %}
"""

class Homepage(clustersetup.ClusterSetup):
    
    def __init__(self):
        self._pool = None

    @property
    def pool(self):
        if self._pool is None:
            self._pool = threadpool.get_thread_pool(20, disable_threads=False)
        return self._pool
        
    def run(self, nodes, master, user, user_shell, volumes):
        pass
        # for node in nodes:
        #     self.pool.simple_job(self.apt_install, (node,), jobid=node.alias)
        # self.pool.wait()

        

        
