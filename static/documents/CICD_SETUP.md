# CI/CD Setup Guide

This guide covers setting up automated deployment for your portfolio website using various CI/CD platforms.

## 📋 Table of Contents

- [Overview](#overview)
- [Generic Deployment Script](#generic-deployment-script)
- [GitHub Actions](#github-actions)
- [GitLab CI/CD](#gitlab-cicd)
- [Jenkins](#jenkins)
- [Custom CI/CD Tools](#custom-cicd-tools)
- [Environment Variables](#environment-variables)
- [Volume Configuration](#volume-configuration)
- [Troubleshooting](#troubleshooting)

## Overview

The portfolio website supports multiple CI/CD platforms through:
- **Generic deployment script** (`scripts/deploy.sh`) - Works with any CI/CD tool
- **Platform-specific configurations** - Optimized workflows for popular platforms
- **Docker-based deployment** - Consistent across all environments
- **Named volumes** - Persistent data without host path dependencies

## Generic Deployment Script

The `scripts/deploy.sh` script can be called from any CI/CD platform.

### Usage

```bash
./scripts/deploy.sh [environment]
```

### Required Environment Variables

Set these in your CI/CD platform:

```bash
export SECRET_KEY="your-secret-key"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD_HASH="your-password-hash"
```

### Optional Environment Variables

```bash
export DOCKER_REGISTRY="ghcr.io/username"  # Default: portfolio-website
export IMAGE_TAG="latest"                   # Default: latest
export PORT="8080"                          # Default: 8080
export BUILD_IMAGE="true"                   # Set to build instead of pull
```

### Example

```bash
# Pull from registry and deploy
export SECRET_KEY="abc123..."
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD_HASH="pbkdf2:sha256..."
export DOCKER_REGISTRY="ghcr.io/hthiers"

./scripts/deploy.sh production
```

## GitHub Actions

### Setup

1. **Copy the workflow file**:
   - File is at `.github/workflows/deploy.yml`
   - Already configured and ready to use

2. **Configure repository secrets** (Settings → Secrets and variables → Actions):

   ```
   SECRET_KEY            - Your Flask secret key
   ADMIN_USERNAME        - Admin username
   ADMIN_PASSWORD_HASH   - Admin password hash
   DEPLOY_HOST           - Your server IP/hostname
   DEPLOY_USER           - SSH username
   DEPLOY_SSH_KEY        - Private SSH key for deployment
   DEPLOY_PORT           - SSH port (optional, default: 22)
   ```

3. **Enable GitHub Container Registry**:
   - Images are automatically pushed to `ghcr.io/[username]/portfolio-website`
   - No additional setup needed

### Trigger Deployment

```bash
# Automatic on push to main/master
git push origin main

# Or manual trigger
# Go to Actions → Deploy Portfolio Website → Run workflow
```

### Workflow Features

- ✅ Builds and pushes Docker image to GHCR
- ✅ Deploys to your server via SSH
- ✅ Uses named volumes (no host path needed)
- ✅ Performs health checks
- ✅ Cleans up old images
- ✅ Build caching for faster builds

## GitLab CI/CD

### Setup

1. **File location**: `.gitlab-ci.yml` (already in project root)

2. **Configure CI/CD variables** (Settings → CI/CD → Variables):

   ```
   SECRET_KEY            - Your Flask secret key
   ADMIN_USERNAME        - Admin username
   ADMIN_PASSWORD_HASH   - Admin password hash
   SSH_PRIVATE_KEY       - Private SSH key (type: File)
   DEPLOY_HOST           - Your server IP/hostname
   DEPLOY_USER           - SSH username
   STAGING_HOST          - Staging server (optional)
   STAGING_SECRET_KEY    - Staging secret key (optional)
   ```

3. **Enable GitLab Container Registry**:
   - Automatically available in GitLab
   - Images pushed to your project's registry

### Environments

- **Production** (`main`/`master` branch):
  - Manual approval required
  - Deploys to port 8080
  - Uses named volume `portfolio-data`

- **Staging** (`develop` branch):
  - Automatic deployment
  - Deploys to port 8081
  - Uses named volume `portfolio-staging-data`

### Trigger Deployment

```bash
# Automatic on push to develop (staging)
git push origin develop

# Production requires manual approval in GitLab UI
git push origin main
# Then: Deployments → Environments → production → Deploy
```

## Jenkins

### Setup

1. **File location**: `Jenkinsfile` (already in project root)

2. **Configure Jenkins credentials** (Manage Jenkins → Credentials):

   | ID | Type | Description |
   |---|---|---|
   | `docker-registry-credentials` | Username/Password | Docker registry login |
   | `portfolio-secret-key` | Secret text | Flask SECRET_KEY |
   | `portfolio-admin-username` | Secret text | Admin username |
   | `portfolio-admin-password-hash` | Secret text | Admin password hash |
   | `deploy-host` | Secret text | Server hostname/IP |
   | `deploy-ssh-credentials` | SSH Username with private key | SSH access |

3. **Create Jenkins Pipeline**:
   - New Item → Pipeline
   - Pipeline → Definition: "Pipeline script from SCM"
   - SCM: Git
   - Script Path: `Jenkinsfile`

### Features

- ✅ Multi-stage pipeline with test stage
- ✅ Pushes to your Docker registry
- ✅ SSH deployment to server
- ✅ Health checks
- ✅ Notifications (ready for Slack/email)
- ✅ Named volume deployment

### Trigger Deployment

- Automatic on SCM changes (if configured)
- Or manual: "Build Now" in Jenkins UI

## Custom CI/CD Tools

For any custom CI/CD tool, use the generic deployment script:

### Deployment Steps

1. **Build the image** (or pull from registry):
   ```bash
   docker build -t portfolio-website:latest .
   ```

2. **Set environment variables**:
   ```bash
   export SECRET_KEY="your-secret-key"
   export ADMIN_USERNAME="admin"
   export ADMIN_PASSWORD_HASH="your-hash"
   ```

3. **Run deployment script**:
   ```bash
   ./scripts/deploy.sh production
   ```

### Example CI/CD Configuration

For tools like CircleCI, Travis CI, Bitbucket Pipelines, etc.:

```yaml
deploy:
  steps:
    - name: Deploy to production
      script: |
        export SECRET_KEY="${SECRET_KEY}"
        export ADMIN_USERNAME="${ADMIN_USERNAME}"
        export ADMIN_PASSWORD_HASH="${ADMIN_PASSWORD_HASH}"
        export DOCKER_REGISTRY="your-registry"
        export IMAGE_TAG="latest"

        chmod +x scripts/deploy.sh
        ./scripts/deploy.sh production
```

### Manual SSH Deployment

If your CI/CD tool has SSH access:

```bash
ssh user@server << 'EOF'
  # Create volume
  docker volume create portfolio-data || true

  # Pull image
  docker pull your-registry/portfolio:latest

  # Stop old container
  docker stop portfolio || true
  docker rm portfolio || true

  # Start new container
  docker run -d \
    --name portfolio \
    --restart unless-stopped \
    -p 8080:8080 \
    -e SECRET_KEY="$SECRET_KEY" \
    -e ADMIN_USERNAME="$ADMIN_USERNAME" \
    -e ADMIN_PASSWORD_HASH="$ADMIN_PASSWORD_HASH" \
    -v portfolio-data:/app/data \
    your-registry/portfolio:latest

  # Health check
  sleep 10
  docker exec portfolio python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/articles')"
EOF
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Flask session secret | `a1b2c3d4e5f6...` |
| `ADMIN_USERNAME` | Admin login username | `admin` |
| `ADMIN_PASSWORD_HASH` | Hashed admin password | `pbkdf2:sha256:...` |

### Optional Variables

| Variable | Description | Default |
|---|---|---|
| `DOCKER_REGISTRY` | Docker registry URL | `portfolio-website` |
| `IMAGE_NAME` | Image name | `portfolio-website` |
| `IMAGE_TAG` | Image tag | `latest` |
| `PORT` | External port | `8080` |
| `BUILD_IMAGE` | Build instead of pull | `false` |

### Generating Credentials

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate PASSWORD_HASH
python generate_password_hash.py
```

## Volume Configuration

### Named Volumes (Recommended for CI/CD)

The deployment uses **named Docker volumes**, which don't require host paths:

```bash
# Volume is created automatically by deploy script
docker volume create portfolio-data
```

**Advantages**:
- ✅ No host path dependencies
- ✅ Works across all CI/CD platforms
- ✅ Docker manages permissions
- ✅ Easy to backup and migrate

### Volume Location

To find where Docker stores the volume:

```bash
docker volume inspect portfolio-data
```

### Backup Named Volume

```bash
# Backup
docker run --rm \
  -v portfolio-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/portfolio-backup.tar.gz -C /data .

# Restore
docker run --rm \
  -v portfolio-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/portfolio-backup.tar.gz -C /data
```

### Alternative: Host Path (Not Recommended for CI/CD)

If you must use a host path:

```bash
docker run -d \
  -v /var/lib/portfolio/data:/app/data \
  ...
```

But this requires:
- Pre-creating the directory
- Managing permissions
- Knowing the host path in advance

## Troubleshooting

### Deployment Script Fails

**Check environment variables**:
```bash
echo $SECRET_KEY
echo $ADMIN_USERNAME
echo $ADMIN_PASSWORD_HASH
```

**Run with debug mode**:
```bash
bash -x scripts/deploy.sh production
```

### Container Won't Start

**Check logs**:
```bash
docker logs portfolio
```

**Common issues**:
- Missing environment variables
- Invalid password hash
- Port already in use

### Volume Issues

**Check volume exists**:
```bash
docker volume ls | grep portfolio
```

**Inspect volume**:
```bash
docker volume inspect portfolio-data
```

**Recreate volume** (⚠️ deletes data):
```bash
docker volume rm portfolio-data
docker volume create portfolio-data
```

### Health Check Fails

**Manual health check**:
```bash
docker exec portfolio python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/articles')"
```

**Check if database initialized**:
```bash
docker exec portfolio ls -la /app/data/
# Should see: portfolio.db
```

**Initialize database manually**:
```bash
docker exec portfolio python -c "from database import init_db; init_db()"
```

### SSH Connection Issues

**Test SSH connection**:
```bash
ssh -i ~/.ssh/your-key user@server
```

**Check SSH key format**:
- Key should be in OpenSSH format
- No passphrase (or configure SSH agent)
- Proper permissions: `chmod 600 ~/.ssh/your-key`

### Registry Authentication

**Docker Hub**:
```bash
docker login
```

**GitHub Container Registry**:
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin
```

**GitLab Container Registry**:
```bash
docker login registry.gitlab.com -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD
```

## Best Practices

1. **Use named volumes** instead of host paths
2. **Store secrets** in your CI/CD platform's secret manager
3. **Enable health checks** to verify deployments
4. **Set resource limits** to prevent resource exhaustion
5. **Clean up old images** regularly
6. **Test in staging** before production
7. **Monitor logs** for errors
8. **Backup database** before major updates
9. **Use image tags** instead of always using `latest`
10. **Set up notifications** for deployment failures

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)

## Need Help?

- Check the [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) guide
- Review [SECURITY_SETUP.md](SECURITY_SETUP.md) for credential management
- Open an issue if you encounter problems
