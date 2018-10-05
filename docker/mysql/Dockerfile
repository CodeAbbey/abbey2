FROM mysql:5.7

EXPOSE 3306

ADD db-init.sql /docker-entrypoint-initdb.d
ENV MYSQL_ROOT_PASSWORD=root
