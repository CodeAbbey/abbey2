FROM mysql:5.7

EXPOSE 3306

ADD *.sql /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD=root
