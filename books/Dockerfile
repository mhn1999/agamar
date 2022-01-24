FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app