sudo docker ps -qa | sudo xargs -n 1 docker stop
sudo docker ps -qa | sudo xargs -n 1 docker rm
