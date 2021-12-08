#Dockerfile - para o aplicativo

FROM python:3.9.9-slim

WORKDIR /spondereServer
COPY /spondereServer/requirements.txt .
RUN pip install -r requirements.txt

COPY . .