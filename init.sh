#!/bin/bash

sudo apt-get update

# install docker
sudo apt install docker.io -y

#3 start docker service
sudo systemctl start docker
sudo systemctl enable docker

# install docker compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

# Change to the project directory
cd /home/ubuntu/MSG

# build and run docker containers
docker-compose up --build