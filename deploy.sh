#!/bin/bash

## Set variables from environment
AWS_REGION=$1
ECR_REGISTRY=$2
ECR_REPOSITORY_NGINX=$3
ECR_REPOSITORY_FLASK=$4
ECR_REPOSITORY_BENTO=$5
VERSION=$6

## Navigate to the directory containing the docker-compose.yml file
echo "Navigating to the Docker Compose directory..."
cd /home/ubuntu/deploy

## Log in to ECR
echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

## Stop running containers and remove them along with their volumes
echo "Stopping and removing existing Docker containers..."
docker-compose down -v

## Clean up Docker resources (images, containers, networks, volumes)
echo "Cleaning up Docker resources..."
docker system prune -a --volumes -f --filter "until=24h"


## Pull images from ECR
echo "Pulling Docker images..."
docker pull $ECR_REGISTRY/$ECR_REPOSITORY_NGINX:$VERSION
docker pull $ECR_REGISTRY/$ECR_REPOSITORY_FLASK:$VERSION
docker pull $ECR_REGISTRY/$ECR_REPOSITORY_BENTO:$VERSION

## Launch the containers and connect the network using docker-compose
echo "Launching the Docker compose with docker-compose-production.yml..."
docker-compose up -d

echo "Deployment completed successfully."
