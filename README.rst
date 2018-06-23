jenkins2sql
===========
A client program used to store subunit test results into a sql database 
optionally tagged with jenkins build parameters
This project uses subunit2sql underneath to insert the subunit streams into
mysql. https://github.com/openstack-infra/subunit2sql

jenkins
-------
1. setup jenkins, for dev you can use the Dockerfile included in this 
repository.
2. install the PostBuildScript plugin
https://wiki.jenkins.io/display/JENKINS/PostBuildScript+Plugin with the jenkins
Plugin Manager
3. create a job that clones your repositories, creates subunit files from your
projects test results, and lastly calls the runs api with the host you 
configured for example: curl -X POST http://myhost/runs?build_url=${BUILD_URL}
using the PostBuildScript plugin mentioned in step 2
 - Instead of using the build_url you can use the project_name and build_number
   variables instead: curl -X POST http://127.0.0.1:7000/runs?"build_url=http://192.168.1.103:8080/job/$JOB_NAME/$BUILD_NUMBER&user=admin&password=admin"

database
--------
1. install mysql: sudo apt-get install mysql-server
2. install python-mysqldb: sudo apt-get install python-mysqldb
3. create db, user, and perform migrations with the tools/test-setup.sh script


for more infromation on the database api you can visit subunit2sql's
api documentation: https://docs.openstack.org/subunit2sql/latest/reference/api.html

frontend
--------
This project does not support a frontend but an example frontend can be
found at https://github.com/openstack/openstack-health

