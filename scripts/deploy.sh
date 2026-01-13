#!/bin/bash
# Generic deployment script for CI/CD pipelines
# Usage: ./scripts/deploy.sh [environment]
#
# This script can be called from any CI/CD tool (GitHub Actions, GitLab CI, Jenkins, etc.)
# Environment variables should be set in your CI/CD platform:
#   - SECRET_KEY
#   - ADMIN_USERNAME
#   - ADMIN_PASSWORD_HASH
#   - DOCKER_REGISTRY (optional, e.g., ghcr.io/username)
#   - IMAGE_TAG (optional, defaults to latest)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-"production"}
IMAGE_NAME="${DOCKER_REGISTRY:-portfolio-website}:${IMAGE_TAG:-latest}"
CONTAINER_NAME="portfolio"
DATA_VOLUME="portfolio-data"
PORT="${PORT:-8080}"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Portfolio Website Deployment${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}Environment: ${ENVIRONMENT}${NC}"
echo -e "${GREEN}Image: ${IMAGE_NAME}${NC}"
echo ""

# Function to check if required env vars are set
check_env_vars() {
    local missing=0

    if [ -z "$SECRET_KEY" ]; then
        echo -e "${RED}❌ SECRET_KEY not set${NC}"
        missing=1
    fi

    if [ -z "$ADMIN_USERNAME" ]; then
        echo -e "${RED}❌ ADMIN_USERNAME not set${NC}"
        missing=1
    fi

    if [ -z "$ADMIN_PASSWORD_HASH" ]; then
        echo -e "${RED}❌ ADMIN_PASSWORD_HASH not set${NC}"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        echo ""
        echo -e "${YELLOW}Set these variables in your CI/CD platform's secrets/environment variables${NC}"
        exit 1
    fi

    echo -e "${GREEN}✓ All required environment variables are set${NC}"
}

# Function to create volume if it doesn't exist
setup_volume() {
    echo ""
    echo -e "${YELLOW}Setting up data volume...${NC}"

    if docker volume inspect $DATA_VOLUME >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Volume '$DATA_VOLUME' already exists${NC}"
    else
        docker volume create $DATA_VOLUME
        echo -e "${GREEN}✓ Created volume '$DATA_VOLUME'${NC}"
    fi
}

# Function to pull or build image
prepare_image() {
    echo ""
    echo -e "${YELLOW}Preparing Docker image...${NC}"

    if [ "$BUILD_IMAGE" = "true" ]; then
        echo "Building image from source..."
        docker build -t $IMAGE_NAME .
        echo -e "${GREEN}✓ Image built successfully${NC}"
    else
        echo "Pulling image from registry..."
        docker pull $IMAGE_NAME
        echo -e "${GREEN}✓ Image pulled successfully${NC}"
    fi
}

# Function to stop and remove existing container
stop_existing() {
    echo ""
    echo -e "${YELLOW}Checking for existing container...${NC}"

    if docker ps -a | grep -q $CONTAINER_NAME; then
        echo "Stopping existing container..."
        docker stop $CONTAINER_NAME || true
        echo "Removing existing container..."
        docker rm $CONTAINER_NAME || true
        echo -e "${GREEN}✓ Existing container removed${NC}"
    else
        echo -e "${GREEN}✓ No existing container found${NC}"
    fi
}

# Function to start new container
start_container() {
    echo ""
    echo -e "${YELLOW}Starting new container...${NC}"

    docker run -d \
        --name $CONTAINER_NAME \
        --restart unless-stopped \
        -p $PORT:8080 \
        -e SECRET_KEY="$SECRET_KEY" \
        -e ADMIN_USERNAME="$ADMIN_USERNAME" \
        -e ADMIN_PASSWORD_HASH="$ADMIN_PASSWORD_HASH" \
        -e FLASK_ENV=production \
        -v $DATA_VOLUME:/app/data \
        $IMAGE_NAME

    echo -e "${GREEN}✓ Container started successfully${NC}"
}

# Function to wait for container to be healthy
wait_for_health() {
    echo ""
    echo -e "${YELLOW}Waiting for application to be ready...${NC}"

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker exec $CONTAINER_NAME python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/articles')" 2>/dev/null; then
            echo -e "${GREEN}✓ Application is healthy!${NC}"
            return 0
        fi

        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done

    echo ""
    echo -e "${RED}❌ Application failed to become healthy${NC}"
    echo "Container logs:"
    docker logs $CONTAINER_NAME
    return 1
}

# Function to show deployment info
show_info() {
    echo ""
    echo -e "${BLUE}================================${NC}"
    echo -e "${GREEN}✅ Deployment Successful!${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
    echo -e "📦 Container: ${GREEN}$CONTAINER_NAME${NC}"
    echo -e "🖼️  Image: ${GREEN}$IMAGE_NAME${NC}"
    echo -e "🌐 Port: ${GREEN}$PORT${NC}"
    echo -e "💾 Volume: ${GREEN}$DATA_VOLUME${NC}"
    echo ""
    echo -e "${YELLOW}Useful commands:${NC}"
    echo -e "  View logs:      docker logs -f $CONTAINER_NAME"
    echo -e "  Check status:   docker ps | grep $CONTAINER_NAME"
    echo -e "  Restart:        docker restart $CONTAINER_NAME"
    echo -e "  Stop:           docker stop $CONTAINER_NAME"
    echo ""
}

# Main deployment flow
main() {
    echo -e "${YELLOW}Step 1/6: Checking environment variables...${NC}"
    check_env_vars

    echo -e "${YELLOW}Step 2/6: Setting up data volume...${NC}"
    setup_volume

    echo -e "${YELLOW}Step 3/6: Preparing Docker image...${NC}"
    prepare_image

    echo -e "${YELLOW}Step 4/6: Stopping existing container...${NC}"
    stop_existing

    echo -e "${YELLOW}Step 5/6: Starting new container...${NC}"
    start_container

    echo -e "${YELLOW}Step 6/6: Verifying deployment...${NC}"
    wait_for_health

    show_info
}

# Error handling
trap 'echo -e "\n${RED}❌ Deployment failed!${NC}"; exit 1' ERR

# Run main deployment
main

exit 0
