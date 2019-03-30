cd /app
pip3 install --no-cache-dir -r py-libs.txt
apk add mariadb mariadb-client curl
mysql_install_db --user=root --datadir=/data
printf "[galera]\nbind-address=0.0.0.0\n[client]\nsocket=/tmp/mysql.sock\n" > /etc/my.cnf
mysqld --user=root --datadir=/data --socket=/tmp/mysql.sock 2>/dev/null &
sleep 3
mysql -e "source db-init.sql;source some-data.sql;"
mysqladmin shutdown

