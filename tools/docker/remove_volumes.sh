sudo docker volume rm $(sudo docker volume ls -qf dangling=true)
