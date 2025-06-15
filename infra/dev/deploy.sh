#!/bin/bash
set -euo pipefail  # Strict error handling

# Log everything for debugging
exec > >(tee /var/log/deployment.log) 2>&1

echo "=== Starting deployment ==="

# System setup
echo "Updating packages..."
sudo apt-get update -y
sudo apt-get install -y docker.io curl unzip

# AWS CLI installation
echo "Installing AWS CLI..."
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
sudo ./aws/install --update
rm awscliv2.zip awscliv2

# Docker configuration
echo "Configuring Docker..."
sudo systemctl enable --now docker
sudo usermod -aG docker ubuntu || true

# Container management
echo "Cleaning up old containers..."
docker stop optionchain-app || true
docker rm optionchain-app || true
docker rm -f $(docker ps -aq) || true

# Image deployment
echo "Loading Docker image..."
aws s3 cp "s3://${S3_BUCKET}/docker-images/${DOCKER_IMAGE}.tar.gz" /tmp/
gunzip -c "/tmp/${DOCKER_IMAGE}.tar.gz" | docker load
rm "/tmp/${DOCKER_IMAGE}.tar.gz"

# Container startup
echo "Starting new container..."
docker run -d \
  -p 80:8501 \
  --name "${DOCKER_IMAGE}" \
  --restart unless-stopped \
  "${DOCKER_IMAGE}:latest"

echo "=== Deployment complete ==="



