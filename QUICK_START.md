# Quick Start Guide

Get your portfolio website running in 5 minutes!

## Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- That's it! 🎉

## Step-by-Step Setup

### 1. Setup Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Generate a secure password (interactive)
python generate_password_hash.py
```

Edit `.env` with your credentials:
```env
SECRET_KEY=<run: python -c "import secrets; print(secrets.token_hex(32))">
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=<paste hash from generate_password_hash.py>
```

### 2. Run with Docker

**Easy way:**
```bash
./scripts/run-local.sh
```

**Or manually:**
```bash
docker-compose up -d
```

### 3. Access Your Website

- 🌐 **Website**: http://localhost:8080
- 🔒 **Admin Panel**: http://localhost:8080/admin
- 👤 **Login**: http://localhost:8080/login

### 4. Seed Database (Optional)

Add sample portfolio articles:

```bash
docker exec -it mywebsite-web-1 python seed_data.py
```

### 5. Customize

1. **Add your info**: Edit `templates/index.html`
2. **Add portfolio items**: Use the admin panel at `/admin`
3. **Upload CV**: Update CV URL in hero section
4. **Add profile picture**: Update image URL in hero section

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop the server
docker-compose down

# Restart after changes
docker-compose restart

# Rebuild from scratch
docker-compose up --build --force-recreate
```

## Default Credentials (Development Only)

⚠️ **Only for local testing! Change before deploying!**

- Username: `admin`
- Password: `changeme`

## Development Mode (with live reload)

```bash
./scripts/run-local.sh dev

# Your site will be at http://localhost:5001
# Code changes will auto-reload
```

## Deploy to Production

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for full deployment guide.

**Quick deploy to Google Cloud Run:**
```bash
./scripts/deploy-gcp.sh your-project-id us-central1
```

## Troubleshooting

### Port already in use
```bash
# Stop existing containers
docker-compose down

# Or use different port in docker-compose.yml
```

### Can't connect to Docker
- Make sure Docker Desktop is running
- Check Docker status: `docker info`

### Database not initializing
```bash
# Initialize manually
docker exec -it mywebsite-web-1 python -c "from database import init_db; init_db()"
```

### Environment variables not loading
```bash
# Verify .env file
cat .env

# Restart containers
docker-compose restart
```

## Need Help?

- **Full Documentation**: See [README.md](README.md)
- **Docker Deployment**: See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
- **Security Setup**: See [SECURITY_SETUP.md](SECURITY_SETUP.md)

## What's Next?

1. ✅ Website running locally
2. 🎨 Customize design and content
3. 📝 Add your portfolio projects via admin panel
4. 🚀 Deploy to production
5. 🌍 Share with the world!

Enjoy your new portfolio website! 🎉
