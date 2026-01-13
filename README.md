# Hernán Thiers - Portfolio Website

Professional portfolio website built with Flask, featuring a dynamic portfolio section powered by SQLite database.

## Features

- Modern, responsive design
- Dynamic portfolio articles stored in SQLite database
- RESTful API endpoints for managing portfolio content
- Clean Python/Flask backend
- No admin panel - manage content via API or direct database access

## Tech Stack

- **Backend**: Python 3.x, Flask 3.0
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Template Engine**: Jinja2

## Project Structure

```
mywebsite/
├── app.py                      # Main Flask application
├── database.py                 # Database operations and models
├── seed_data.py               # Script to populate initial data
├── requirements.txt           # Python dependencies
├── portfolio.db              # SQLite database (generated)
├── templates/
│   └── index.html           # Main page template
└── static/                  # Static files (if needed)
```

## Setup Instructions

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

## Deployment

### Option 1: Railway

1. Create a `runtime.txt`:
   ```
   python-3.11.0
   ```

2. Create a `Procfile`:
   ```
   web: python app.py
   ```

3. Push to Railway and deploy

### Option 2: Render

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`

### Option 3: Traditional Hosting (cPanel, etc.)

1. Upload files via FTP
2. Configure Python application in cPanel
3. Point to `app.py` as the entry point

## Development

To add new features:

1. Modify `database.py` for database operations
2. Add routes in `app.py`
3. Update templates in `templates/`

## License

All rights reserved - Hernán Thiers 2026

## Support

For issues or questions, contact via the methods listed on the website
