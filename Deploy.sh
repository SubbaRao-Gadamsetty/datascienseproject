#!/bin/bash

DOCKER_USER="subbaraogadamsetty"

# Pull latest image from Docker Hub
echo "🔄 Pulling latest Docker image..."
docker pull $DOCKER_USER/california-api:latest

# Stop and remove existing container
echo "🛑 Stopping existing container (if any)..."
docker stop california-api || true
docker rm california-api || true

# Run new container
echo "🚀 Starting new container..."
docker run -d -p 8080:8080 --name california-api $DOCKER_USER/california-api:latest
