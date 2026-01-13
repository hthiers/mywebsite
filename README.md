# Hernán Thiers - Portfolio Website

Professional portfolio website built with Flask, featuring a dynamic portfolio section with bilingual support (Spanish/English) and secure admin panel.

## Features

- 🎨 Modern, responsive design with full-width sections
- 🌐 Bilingual support (Spanish/English) with client-side language switching
- 📝 Secure admin panel for managing portfolio articles
- 🔒 Authentication system with password hashing
- 🗄️ Dynamic portfolio articles stored in SQLite database
- 🚀 RESTful API endpoints for content management
- 🐳 Docker support for easy deployment
- 📱 Mobile-first responsive design

## Tech Stack

- **Backend**: Python 3.11+, Flask 3.0
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Template Engine**: Jinja2
- **Deployment**: Docker, Gunicorn
- **Security**: Werkzeug password hashing, Flask sessions

## Project Structure

```
mywebsite/
├── app.py                         # Main Flask application
├── database.py                    # Database operations and models
├── seed_data.py                  # Script to populate initial data
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Production Docker image
├── Dockerfile.dev               # Development Docker image
├── docker-compose.yml           # Docker Compose configuration
├── .dockerignore                # Docker build exclusions
├── .env.example                 # Environment variables template
├── templates/
│   ├── index.html              # Main website template
│   ├── admin.html              # Admin panel
│   └── login.html              # Login page
├── data/                        # Database directory (created automatically)
│   └── portfolio.db            # SQLite database
├── scripts/                     # Deployment helper scripts
│   ├── deploy-gcp.sh           # Google Cloud Run deployment
│   ├── run-local.sh            # Local Docker runner
│   └── build-and-push.sh       # Build and push to registry
└── static/
    └── documents/               # Static files (CV, images)
```

## Quick Start (Docker - Recommended)

The easiest way to run the website is using Docker:

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- Git (to clone the repository)

### 2. Setup Environment
```bash
# Clone or navigate to project
cd mywebsite

# Copy environment template
cp .env.example .env

# Generate secure credentials
python generate_password_hash.py
```

Edit `.env` file with your credentials (see [SECURITY_SETUP.md](SECURITY_SETUP.md) for details).

### 3. Run with Docker

**Production mode:**
```bash
./scripts/run-local.sh prod
# Or: docker-compose up -d
```

**Development mode (with live reload):**
```bash
./scripts/run-local.sh dev
# Or: docker-compose --profile dev up dev
```

### 4. Access the Website

- **Website**: http://localhost:8080
- **Admin Panel**: http://localhost:8080/admin
- **Login**: http://localhost:8080/login

**Default credentials** (for testing only):
- Username: `admin`
- Password: `changeme`

⚠️ **Change these before deploying to production!**

### 5. Seed Database (Optional)

```bash
docker exec -it mywebsite-web-1 python seed_data.py
```

## Setup Instructions (Without Docker)

### 1. Clone or navigate to the project directory

```bash
cd /Users/hernanthiers/Workspace/mywebsite
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database with seed data

```bash
python seed_data.py
```

This will create the SQLite database and populate it with the three initial portfolio articles.

### 5. Run the application

```bash
python app.py
```

The application will start on `http://localhost:5001`

## Usage

### Viewing the Website

Simply open your browser and navigate to:
```
http://localhost:5001
```

### API Endpoints

All API endpoints return JSON responses.

#### Get all portfolio articles
```http
GET /api/articles
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Relok - Sistema de Control de Tiempos",
    "description": "Aplicación web desarrollada para gestión...",
    "image_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "image_letter": "R",
    "tech_stack": ["Laravel", "React", "MySQL", "Docker"],
    "created_at": "2026-01-12 10:30:00",
    "updated_at": "2026-01-12 10:30:00"
  }
]
```

#### Get a single article
```http
GET /api/articles/<id>
```

#### Create a new article
```http
POST /api/articles
Content-Type: application/json

{
  "title": "New Project",
  "description": "Project description here",
  "tech_stack": ["Python", "Flask", "SQLite"],
  "image_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  "image_letter": "N"
}
```

**Note:** `image_gradient` and `image_letter` are optional fields.

#### Update an article
```http
PUT /api/articles/<id>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "tech_stack": ["Python", "Flask"]
}
```

#### Delete an article
```http
DELETE /api/articles/<id>
```

### API Examples with curl

**Get all articles:**
```bash
curl http://localhost:5001/api/articles
```

**Create a new article:**
```bash
curl -X POST http://localhost:5001/api/articles \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Chatbot Platform",
    "description": "Plataforma de chatbots con IA para atención al cliente automatizada.",
    "tech_stack": ["Python", "FastAPI", "OpenAI", "Redis"],
    "image_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "image_letter": "AI"
  }'
```

**Update an article:**
```bash
curl -X PUT http://localhost:5001/api/articles/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Project Title",
    "description": "Updated description",
    "tech_stack": ["Python", "Flask", "PostgreSQL"]
  }'
```

**Delete an article:**
```bash
curl -X DELETE http://localhost:5001/api/articles/1
```

## Database Schema

### portfolio_articles table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| title | TEXT | Article title |
| description | TEXT | Article description |
| image_gradient | TEXT | CSS gradient for card background |
| image_letter | TEXT | Letter or emoji to display on card |
| tech_stack | TEXT | JSON array of technologies used |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

## Customization

### Adding Your Personal Information

Edit `templates/index.html` to update:
- Your name and contact information
- GitHub profile links
- WhatsApp number
- Email address
- Credentials and diplomas

### Styling

All CSS is embedded in `templates/index.html`. You can:
- Modify color variables in the `:root` section
- Adjust fonts and sizes
- Change gradients and animations

## Production Deployment

### Option 1: Google Cloud Run (Recommended)

Serverless, auto-scaling, and cost-effective:

```bash
# Deploy using helper script
./scripts/deploy-gcp.sh your-project-id us-central1

# Or manually:
gcloud builds submit --tag gcr.io/your-project-id/portfolio
gcloud run deploy portfolio --image gcr.io/your-project-id/portfolio \
  --platform managed --region us-central1 --allow-unauthenticated
```

See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed instructions.

### Option 2: AWS, DigitalOcean, or any VPS

Deploy using Docker on any cloud provider:

```bash
# Build and push to registry
./scripts/build-and-push.sh your-registry/portfolio:latest

# Deploy on your server
ssh user@your-server
docker pull your-registry/portfolio:latest
docker run -d -p 80:8080 --env-file .env your-registry/portfolio:latest
```

### Option 3: Traditional Hosting

For platforms without Docker support:

1. Install Python 3.11+ on the server
2. Upload files via Git or FTP
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables
5. Run with Gunicorn: `gunicorn -w 2 -b 0.0.0.0:8080 app:app`

### Environment Variables for Production

Make sure to set these in your deployment platform:

```env
SECRET_KEY=<your-generated-secret-key>
ADMIN_USERNAME=<your-admin-username>
ADMIN_PASSWORD_HASH=<your-generated-password-hash>
```

**Never use the default credentials in production!**

See [SECURITY_SETUP.md](SECURITY_SETUP.md) for security best practices.

## Development

To add new features:

1. Modify `database.py` for database operations
2. Add routes in `app.py`
3. Update templates in `templates/`

## License

All rights reserved - Hernán Thiers 2026

## Support

For issues or questions, contact via the methods listed on the website
