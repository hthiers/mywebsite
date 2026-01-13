#!/bin/bash
# Build and push Docker image to registry
# Usage: ./scripts/build-and-push.sh [registry/image:tag]

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Default image name
IMAGE_NAME=${1:-"portfolio-website:latest"}

echo -e "${GREEN}Building Docker image: ${IMAGE_NAME}${NC}"

# Build the image
docker build -t ${IMAGE_NAME} .

if [ $? -ne 0 ]; then
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful!${NC}"
echo ""

# Ask if user wants to push
read -p "Push to registry? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing ${IMAGE_NAME} to registry...${NC}"
    docker push ${IMAGE_NAME}

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully pushed to registry!${NC}"
    else
        echo -e "${RED}Push failed. Make sure you're logged in to the registry.${NC}"
        echo ""
        echo "Login commands:"
        echo "  Docker Hub: docker login"
        echo "  Google Cloud: gcloud auth configure-docker"
        echo "  AWS ECR: aws ecr get-login-password | docker login --username AWS --password-stdin [registry-url]"
        exit 1
    fi
else
    echo "Skipping push to registry"
fi

echo ""
echo -e "${GREEN}Image ready: ${IMAGE_NAME}${NC}"
echo ""
echo "Run locally:"
echo "  docker run -p 8080:8080 --env-file .env ${IMAGE_NAME}"
