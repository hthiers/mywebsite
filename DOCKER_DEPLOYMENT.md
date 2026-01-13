# Docker Deployment Guide

This guide covers building and deploying your portfolio website using Docker.

## 📦 What's Included

- **Dockerfile** - Multi-stage production-optimized image
- **Dockerfile.dev** - Development image with live reload
- **docker-compose.yml** - Orchestration for local and production deployment
- **.dockerignore** - Excludes unnecessary files from the image

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

### 1. Local Development (with live reload)

```bash
# Run development server
docker-compose --profile dev up dev

# Your site will be available at http://localhost:5001
# Changes to code will automatically reload
```

### 2. Production Mode (locally)

```bash
# Build and run production container
docker-compose up --build

# Your site will be available at http://localhost:8080
```

### 3. Stop Containers

```bash
# Stop running containers
docker-compose down

# Stop and remove volumes (database will be deleted)
docker-compose down -v
```

## 🏗️ Building the Docker Image

### Build Production Image

```bash
# Build the image
docker build -t portfolio-website:latest .

# Run the container
docker run -d \
  -p 8080:8080 \
  -e SECRET_KEY="your-secret-key" \
  -e ADMIN_USERNAME="admin" \
  -e ADMIN_PASSWORD_HASH="your-password-hash" \
  -v $(pwd)/data:/app/data \
  --name portfolio \
  portfolio-website:latest
```

### Build Development Image

```bash
# Build development image
docker build -f Dockerfile.dev -t portfolio-website:dev .

# Run development container
docker run -d \
  -p 5001:5001 \
  -v $(pwd):/app \
  --name portfolio-dev \
  portfolio-website:dev
```

## 🌐 Production Deployment

### Option 1: Google Cloud Run

Google Cloud Run is serverless, auto-scaling, and cost-effective.

```bash
# 1. Set your project ID
export PROJECT_ID="your-project-id"

# 2. Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/${PROJECT_ID}/portfolio-website

# 3. Deploy to Cloud Run
gcloud run deploy portfolio-website \
  --image gcr.io/${PROJECT_ID}/portfolio-website \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "SECRET_KEY=your-secret-key" \
  --set-env-vars "ADMIN_USERNAME=admin" \
  --set-env-vars "ADMIN_PASSWORD_HASH=your-hash"

# 4. Note: For persistent database, mount Google Cloud Storage
# or use Cloud SQL for PostgreSQL
```

### Option 2: AWS Elastic Container Service (ECS)

```bash
# 1. Authenticate Docker to AWS ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# 2. Create ECR repository
aws ecr create-repository --repository-name portfolio-website

# 3. Build and tag image
docker build -t portfolio-website .
docker tag portfolio-website:latest \
  YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/portfolio-website:latest

# 4. Push to ECR
docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/portfolio-website:latest

# 5. Create ECS task definition and service via AWS Console or CLI
# Set environment variables in task definition
```

### Option 3: DigitalOcean App Platform

```bash
# 1. Install doctl CLI
brew install doctl  # macOS

# 2. Authenticate
doctl auth init

# 3. Build and push to DigitalOcean Container Registry
doctl registry login
docker build -t registry.digitalocean.com/your-registry/portfolio-website .
docker push registry.digitalocean.com/your-registry/portfolio-website

# 4. Deploy via DigitalOcean dashboard or create app spec YAML
```

### Option 4: Traditional VPS (DigitalOcean, Linode, AWS EC2)

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Clone your repository
git clone https://github.com/yourusername/portfolio.git
cd portfolio

# 4. Create .env file with your credentials
nano .env

# 5. Run with docker-compose
docker-compose up -d

# 6. Setup nginx reverse proxy (recommended)
# See nginx configuration below
```

## 🔒 Environment Variables for Production

Create a `.env` file or set environment variables in your deployment platform:

```env
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<generate with: python generate_password_hash.py>
```

**Important**: Never commit `.env` to version control!

## 🗄️ Database Persistence

The SQLite database needs to persist between container restarts.

### Using Docker Volumes

```bash
# Create a named volume
docker volume create portfolio-data

# Run container with volume
docker run -d \
  -p 8080:8080 \
  -v portfolio-data:/app/data \
  portfolio-website:latest
```

### Using Host Directory

```bash
# Mount local directory
docker run -d \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  portfolio-website:latest
```

### Cloud Storage Options

For production, consider:
- **Google Cloud Run**: Mount Google Cloud Storage bucket
- **AWS**: Use EFS (Elastic File System) or RDS
- **DigitalOcean**: Use Spaces or Managed Databases

## 🌍 Nginx Reverse Proxy (VPS Deployment)

If deploying to a VPS, use nginx as a reverse proxy:

```nginx
# /etc/nginx/sites-available/portfolio
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart nginx:

```bash
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Add SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

## 🔍 Monitoring and Logs

### View Container Logs

```bash
# Follow logs
docker-compose logs -f

# View specific service logs
docker logs portfolio

# Last 100 lines
docker logs --tail 100 portfolio
```

### Health Checks

The Docker image includes a health check that pings `/api/articles`:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' portfolio
```

## 🛠️ Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Check if port is already in use
lsof -i :8080

# Rebuild without cache
docker-compose build --no-cache
```

### Database Issues

```bash
# Initialize database manually
docker exec -it portfolio python -c "from database import init_db; init_db()"

# Seed with sample data
docker exec -it portfolio python seed_data.py
```

### Permission Issues

```bash
# Fix data directory permissions
sudo chown -R 1000:1000 ./data
```

### Environment Variables Not Loading

```bash
# Verify .env file exists
ls -la .env

# Check if variables are set in container
docker exec portfolio env | grep ADMIN
```

## 📊 Performance Optimization

### Production Settings

The production Dockerfile includes:
- **Gunicorn** with 2 workers and 4 threads
- **Non-root user** for security
- **Health checks** for monitoring
- **Multi-stage build** for smaller image size

### Scaling with Docker Compose

```yaml
# docker-compose.yml
services:
  web:
    deploy:
      replicas: 3  # Run 3 instances
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## 🔄 CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build and push Docker image
        run: |
          docker build -t your-registry/portfolio:latest .
          docker push your-registry/portfolio:latest

      - name: Deploy to production
        run: |
          # Your deployment commands here
```

## 🔐 Security Best Practices

1. **Use secrets management**: Store credentials in Docker secrets or cloud provider's secret manager
2. **Run as non-root**: The Dockerfile already configures this
3. **Keep images updated**: Regularly rebuild with latest base images
4. **Use HTTPS**: Always use SSL/TLS in production
5. **Limit resources**: Set CPU/memory limits in docker-compose
6. **Scan for vulnerabilities**: Use `docker scan portfolio-website`

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [DigitalOcean App Platform](https://docs.digitalocean.com/products/app-platform/)

## 🆘 Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify environment variables are set correctly
3. Ensure database directory has correct permissions
4. Try rebuilding without cache: `docker-compose build --no-cache`
5. Check firewall rules allow traffic on ports 8080 or 80/443
