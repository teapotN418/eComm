# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt ./requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# create log directory
RUN mkdir -p /var/log/minio_service

# copy project
COPY . ./

# Starting the app
ENTRYPOINT ["sh", "-c", "uvicorn src.app.main:app --port 8000 --host 0.0.0.0 2>&1 | tee -a /var/log/minio_service/app.log"]
    #"--ssl-certfile", "fullchain.pem", "--ssl-keyfile", "privkey.pem"]