from flask import Flask, render_template, request, jsonify
from database import (
    init_db, get_all_articles, get_article_by_id,
    create_article, update_article, delete_article
)
import os

app = Flask(__name__)

# Initialize database on first run
if not os.path.exists('portfolio.db'):
    init_db()

@app.route('/')
def index():
    """Render the main page with all portfolio articles."""
    articles = get_all_articles()
    return render_template('index.html', articles=articles)

@app.route('/admin')
def admin():
    """Admin interface for managing portfolio articles."""
    return render_template('admin.html')

# API Endpoints

@app.route('/api/articles', methods=['GET'])
def api_get_articles():
    """Get all portfolio articles as JSON."""
    articles = get_all_articles()
    return jsonify(articles)

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def api_get_article(article_id):
    """Get a single portfolio article by ID."""
    article = get_article_by_id(article_id)
    if article is None:
        return jsonify({'error': 'Article not found'}), 404
    return jsonify(article)

@app.route('/api/articles', methods=['POST'])
def api_create_article():
    """Create a new portfolio article.

    Expected JSON body:
    {
        "title": "Project Title (Spanish)",
        "description": "Project description (Spanish)",
        "title_en": "Project Title (English)",  # optional
        "description_en": "Project description (English)",  # optional
        "tech_stack": ["Python", "Flask", "SQLite"],
        "image_url": "https://example.com/image.jpg",  # optional
        "image_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",  # optional
        "image_letter": "P"  # optional
    }
    """
    data = request.get_json()

    if not data or 'title' not in data or 'description' not in data or 'tech_stack' not in data:
        return jsonify({'error': 'Missing required fields: title, description, tech_stack'}), 400

    title = data['title']
    description = data['description']
    tech_stack = data['tech_stack']
    image_gradient = data.get('image_gradient', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)')
    image_letter = data.get('image_letter', '')
    title_en = data.get('title_en')
    description_en = data.get('description_en')
    image_url = data.get('image_url')

    article_id = create_article(title, description, tech_stack, image_gradient, image_letter, title_en, description_en, image_url)

    return jsonify({
        'message': 'Article created successfully',
        'id': article_id
    }), 201

@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def api_update_article(article_id):
    """Update an existing portfolio article.

    Expected JSON body:
    {
        "title": "Updated Title (Spanish)",
        "description": "Updated description (Spanish)",
        "title_en": "Updated Title (English)",  # optional
        "description_en": "Updated description (English)",  # optional
        "tech_stack": ["Python", "Flask"],
        "image_url": "https://example.com/image.jpg",  # optional
        "image_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",  # optional
        "image_letter": "U"  # optional
    }
    """
    data = request.get_json()

    if not data or 'title' not in data or 'description' not in data or 'tech_stack' not in data:
        return jsonify({'error': 'Missing required fields: title, description, tech_stack'}), 400

    title = data['title']
    description = data['description']
    tech_stack = data['tech_stack']
    image_gradient = data.get('image_gradient')
    image_letter = data.get('image_letter')
    title_en = data.get('title_en')
    description_en = data.get('description_en')
    image_url = data.get('image_url')

    success = update_article(article_id, title, description, tech_stack, image_gradient, image_letter, title_en, description_en, image_url)

    if not success:
        return jsonify({'error': 'Article not found or update failed'}), 404

    return jsonify({
        'message': 'Article updated successfully',
        'id': article_id
    })

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def api_delete_article(article_id):
    """Delete a portfolio article."""
    success = delete_article(article_id)

    if not success:
        return jsonify({'error': 'Article not found'}), 404

    return jsonify({
        'message': 'Article deleted successfully',
        'id': article_id
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
