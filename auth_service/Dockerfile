FROM python:3.11.1-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT ["uvicorn", "src.app.main:app", "--port", "8000", "--host", "0.0.0.0"]
