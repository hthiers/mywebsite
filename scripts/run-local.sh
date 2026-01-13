#!/bin/bash
# Run portfolio website locally with Docker
# Usage: ./scripts/run-local.sh [dev|prod]

set -e

MODE=${1:-"prod"}

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting portfolio website in ${MODE} mode...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo -e "${YELLOW}⚠️  Please edit .env file with your credentials before continuing${NC}"
    echo "Run: nano .env"
    exit 1
fi

# Stop any running containers
echo "Stopping any existing containers..."
docker-compose down 2>/dev/null || true

if [ "$MODE" = "dev" ]; then
    echo -e "${GREEN}Starting development server with live reload...${NC}"
    docker-compose --profile dev up --build dev
    echo ""
    echo -e "${GREEN}Development server running at http://localhost:5001${NC}"
else
    echo -e "${GREEN}Starting production server...${NC}"
    docker-compose up --build -d

    echo ""
    echo -e "${GREEN}✅ Production server running!${NC}"
    echo ""
    echo -e "🌐 Website: ${GREEN}http://localhost:8080${NC}"
    echo -e "🔒 Admin: ${GREEN}http://localhost:8080/admin${NC}"
    echo ""
    echo -e "📋 View logs: ${YELLOW}docker-compose logs -f${NC}"
    echo -e "🛑 Stop server: ${YELLOW}docker-compose down${NC}"
fi
