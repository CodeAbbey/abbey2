FROM python:3.7

EXPOSE 5000

RUN mkdir /app
RUN ln -s /code /app/code
WORKDIR /app
COPY py-libs.txt run.sh ./
RUN pip3 install --no-cache-dir -r py-libs.txt

ENV PYTHONDONTWRITEBYTECODE=1
CMD ./run.sh
