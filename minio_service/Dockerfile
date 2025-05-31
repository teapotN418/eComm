# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVICE_NAME=minio_service

# install dependencies
COPY ./requirements.txt ./requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# copy project
COPY . ./

# Starting the app
ENTRYPOINT ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]