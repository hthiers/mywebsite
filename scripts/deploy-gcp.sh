#!/bin/bash
# Deploy to Google Cloud Run
# Usage: ./scripts/deploy-gcp.sh [project-id] [region]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
SERVICE_NAME="portfolio-website"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo -e "${GREEN}Starting deployment to Google Cloud Run...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Create .env file with your credentials first"
    exit 1
fi

# Load environment variables
source .env

# Validate required environment variables
if [ -z "$SECRET_KEY" ] || [ -z "$ADMIN_USERNAME" ] || [ -z "$ADMIN_PASSWORD_HASH" ]; then
    echo -e "${RED}Error: Required environment variables not set${NC}"
    echo "Make sure SECRET_KEY, ADMIN_USERNAME, and ADMIN_PASSWORD_HASH are set in .env"
    exit 1
fi

# Set active project
echo -e "${YELLOW}Setting GCP project to ${PROJECT_ID}...${NC}"
gcloud config set project ${PROJECT_ID}

# Build and submit to Google Cloud Build
echo -e "${YELLOW}Building Docker image...${NC}"
gcloud builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "SECRET_KEY=${SECRET_KEY}" \
  --set-env-vars "ADMIN_USERNAME=${ADMIN_USERNAME}" \
  --set-env-vars "ADMIN_PASSWORD_HASH=${ADMIN_PASSWORD_HASH}"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --format 'value(status.url)')

echo ""
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo ""
echo -e "🌐 Your website is live at: ${GREEN}${SERVICE_URL}${NC}"
echo -e "🔒 Admin panel: ${GREEN}${SERVICE_URL}/admin${NC}"
echo ""
echo -e "${YELLOW}Note: For persistent database, consider using Cloud SQL or Cloud Storage${NC}"
