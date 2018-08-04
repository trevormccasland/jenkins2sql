===========
jenkins2sql
===========
A framework to store subunit test results into a sql database tagged with
jenkins build parameters
This project uses subunit2sql underneath to insert the subunit streams into
mysql. https://github.com/openstack-infra/subunit2sql

developer setup
===============

jenkins container
-----------------
#. setup jenkins, for dev you can use the Dockerfile included in this repository. If you want to use the tools/docker scripts, tag the image as ``myjenkins``
#. install the PostBuildScript_ plugin with the jenkins Plugin Manager.
#. create a job that clones your repositories, creates subunit files from your
   projects test results, and lastly calls the runs api with the host you
   configured for example: curl -X POST http://myhost/runs?build_url=${BUILD_URL}
   using the PostBuildScript_ plugin mentioned in step 2

.. note:: Instead of using the build_url you can use the project_name and build_number
          variables: curl -X POST http://127.0.0.1:7000/runs?"build_url=http://192.168.1.103:8080/job/$JOB_NAME/$BUILD_NUMBER&user=admin&password=admin"

database
--------
#. install mysql: sudo apt-get install mysql-server
#. install python-mysqldb: sudo apt-get install python-mysqldb
#. create db, user, and perform migrations with the tools/test-setup.sh script


for more infromation on the database api you can visit subunit2sql's
api documentation_

frontend
--------
This project does not support a frontend but an example frontend can be
found at https://github.com/openstack/openstack-health

.. _PostBuildScript: https://wiki.jenkins.io/display/JENKINS/PostBuildScript+Plugin
.. _documentation: https://docs.openstack.org/subunit2sql/latest/reference/api.html
.. _openstack-health: https://github.com/openstack/openstack-health

openstack-health install
^^^^^^^^^^^^^^^^^^^^^^^^
::

  git clone https://github.com/openstack/openstack-health
  cd openstack-health
  pip install -r requirements.txt
  pip install -e .
  curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
  sudo apt-get install -y nodejs
  sudo npm -g config set prefix /usr/local
  sudo npm -g install npm
  sudo npm -g install gulp
  npm install

openstack-health usage
^^^^^^^^^^^^^^^^^^^^^^

::

  openstack-health-api jenkins2sql/etc/openstack-health-api.conf
  sudo gulp dev
