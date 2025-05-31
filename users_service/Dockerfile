# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVICE_NAME=users_service

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# create log directory and set permissions
RUN mkdir -p /var/log/users_service && \
    chmod 777 /var/log/users_service

# copy project
COPY . ./

# Starting the app
ENTRYPOINT ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
#    "--ssl-certfile", "fullchain.pem", "--ssl-keyfile", "privkey.pem"]