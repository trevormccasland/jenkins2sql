#!/bin/bash -xe

# This setup needs to be run as a user that can run sudo.

# The root password for the MySQL database; pass it in via
# MYSQL_ROOT_PW.
DB_ROOT_PW=${MYSQL_ROOT_PW:-jenkins}

# This user and its password are used by the tests, if you change it,
# your tests might fail.
DB_USER=citest
DB_PW=citest
DB_NAME=citest
DB_HOST=localhost

# It's best practice to remove anonymous users from the database.  If
# a anonymous user exists, then it matches first for connections and
# other connections from that host will not work.
sudo -H mysql -u root -p$DB_ROOT_PW -h $DB_HOST -e "
    DELETE FROM mysql.user WHERE User='';
    DELETE FROM mysql.user WHERE User='$DB_USER';
    DROP USER IF EXISTS $DB_USER@$DB_HOST;
    FLUSH PRIVILEGES;
    GRANT ALL PRIVILEGES ON *.*
        TO '$DB_USER'@'$DB_HOST' identified by '$DB_PW' WITH GRANT OPTION;"

# Now create our database.
sudo mysql -u root -p$DB_ROOT_PW -h $DB_HOST -e "
    SET default_storage_engine=MYISAM;
    DROP DATABASE IF EXISTS $DB_NAME;
    CREATE DATABASE $DB_NAME CHARACTER SET utf8;"

# Create users
#sudo -H mysql -u root -p$DB_ROOT_PW -h $DB_HOST -e "
#    CREATE USER '$DB_USER'@'$DB_HOST' IDENTIFIED BY '$DB_PW';
#    GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_NAME'@'$DB_HOST';
#    FLUSH PRIVILEGES;"

subunit2sql-db-manage --database-connection mysql+pymysql://$DB_USER:$DB_PW@$DB_HOST/$DB_NAME upgrade head
