FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /federated_learning_auto_upload

COPY . .

RUN cp sources.list /etc/apt \
    && apt-get update -y --no-install-recommends \
    && apt-get install -y python3-pip python3-dev openssh-server openssh-client\
    && pip3 install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt \
    && apt install openssh-server 
