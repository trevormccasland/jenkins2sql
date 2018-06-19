# jenkins2sql
A client program used to store subunit test results into a sql database 
optionally tagged with jenkins build parameters

## jenkins
1. setup jenkins, for dev you can use https://github.com/buulam/jenkins-docker-pip
2. install the PostBuildScript plugin
https://wiki.jenkins.io/display/JENKINS/PostBuildScript+Plugin with the jenkins
Plugin Manager
3. create a job that clones your repositories, creates subunit files from your
projects test results, and lastly calls the runs api with the host you 
configured for example: curl -X POST http://myhost/runs?build_url=${BUILD_URL}

## database
1. install mysql: sudo apt-get install mysql-server
2. perform migrations with the /tools/setup-db.sh script
3. create users

