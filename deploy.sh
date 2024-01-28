#!/bin/bash

## Set variables from environment
AWS_REGION=$1
AWS_ACCOUNT_ID=$2
ECR_REPOSITORY_NGINX=$3
ECR_REPOSITORY_FLASK=$4
ECR_REPOSITORY_BENTO=$5
VERSION=$6

## Navigate to the directory containing the docker-compose.yml file
echo "Navigating to the Docker Compose directory..."
cd /home/ubuntu/deploy

## Log in to ECR
echo "Logging in to Amazon ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

## Stop running containers and remove them along with their volumes
echo "Stopping and removing existing Docker containers..."
docker-compose down -v || echo "No running containers to stop."

## Clean up Docker resources (images, containers, networks, volumes)
echo "Cleaning up Docker resources..."
docker system prune -a --volumes -f


## Pull images from ECR
echo "Pulling Docker images..."
docker pull $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NGINX:$VERSION
docker pull $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_FLASK:$VERSION
docker pull $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_BENTO:$VERSION

## Launch the containers and connect the network using docker-compose
echo "Launching the Docker compose with docker-compose-production.yml..."
docker-compose -f docker-compose-production.yml up -d

echo "Deployment completed successfully."
