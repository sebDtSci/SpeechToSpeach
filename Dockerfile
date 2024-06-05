FROM ubuntu:latest

RUN apt-get update 

RUN apt-get install -y git

RUN apt-get install -y python3-pip

WORKDIR /usr/src/app

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt