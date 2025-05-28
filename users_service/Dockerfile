# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . ./

# Starting the app
ENTRYPOINT ["uvicorn" "src.app.main:app" "--port" "8000" "--host" "0.0.0.0"]