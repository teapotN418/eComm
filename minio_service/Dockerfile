FROM python:3.11.1-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# create log directory
RUN mkdir -p /var/log/minio_service

COPY . ./

ENTRYPOINT ["uvicorn", "src.app.main:app", "--port", "8000", "--host", "0.0.0.0"]
