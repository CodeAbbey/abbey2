FROM python:3.7-alpine

EXPOSE 5000

WORKDIR /app

COPY ["py-libs.txt","db-init.sql","some-data.sql","init.sh","run.sh","/app/"]

RUN source /app/init.sh

CMD source /app/run.sh
