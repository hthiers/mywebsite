import sqlite3
import json
from typing import List, Optional, Dict

DATABASE = 'portfolio.db'

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the portfolio_articles table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            title_en TEXT,
            description_en TEXT,
            image_url TEXT,
            image_gradient TEXT DEFAULT 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            image_letter TEXT DEFAULT '',
            tech_stack TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_all_articles() -> List[Dict]:
    """Get all portfolio articles."""
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM portfolio_articles ORDER BY created_at DESC').fetchall()
    conn.close()

    result = []
    for article in articles:
        result.append({
            'id': article['id'],
            'title': article['title'],
            'description': article['description'],
            'title_en': article['title_en'] if article['title_en'] else article['title'],
            'description_en': article['description_en'] if article['description_en'] else article['description'],
            'image_url': article['image_url'],
            'image_gradient': article['image_gradient'],
            'image_letter': article['image_letter'],
            'tech_stack': json.loads(article['tech_stack']) if article['tech_stack'] else [],
            'created_at': article['created_at'],
            'updated_at': article['updated_at']
        })

    return result

def get_article_by_id(article_id: int) -> Optional[Dict]:
    """Get a single portfolio article by ID."""
    conn = get_db_connection()
    article = conn.execute('SELECT * FROM portfolio_articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()

    if article is None:
        return None

    return {
        'id': article['id'],
        'title': article['title'],
        'description': article['description'],
        'title_en': article['title_en'] if article['title_en'] else article['title'],
        'description_en': article['description_en'] if article['description_en'] else article['description'],
        'image_url': article['image_url'],
        'image_gradient': article['image_gradient'],
        'image_letter': article['image_letter'],
        'tech_stack': json.loads(article['tech_stack']) if article['tech_stack'] else [],
        'created_at': article['created_at'],
        'updated_at': article['updated_at']
    }

def create_article(title: str, description: str, tech_stack: List[str],
                  image_gradient: str = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  image_letter: str = '',
                  title_en: str = None,
                  description_en: str = None,
                  image_url: str = None) -> int:
    """Create a new portfolio article."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # If English translations not provided, use Spanish as fallback
    if title_en is None:
        title_en = title
    if description_en is None:
        description_en = description

    cursor.execute('''
        INSERT INTO portfolio_articles (title, description, title_en, description_en, image_url, image_gradient, image_letter, tech_stack)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, title_en, description_en, image_url, image_gradient, image_letter, json.dumps(tech_stack)))

    article_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return article_id

def update_article(article_id: int, title: str, description: str, tech_stack: List[str],
                  image_gradient: str = None, image_letter: str = None,
                  title_en: str = None, description_en: str = None,
                  image_url: str = None) -> bool:
    """Update an existing portfolio article."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build dynamic SQL based on which fields are provided
    update_fields = ['title = ?', 'description = ?', 'tech_stack = ?']
    values = [title, description, json.dumps(tech_stack)]

    if title_en is not None:
        update_fields.append('title_en = ?')
        values.append(title_en)

    if description_en is not None:
        update_fields.append('description_en = ?')
        values.append(description_en)

    if image_url is not None:
        update_fields.append('image_url = ?')
        values.append(image_url)

    if image_gradient is not None:
        update_fields.append('image_gradient = ?')
        values.append(image_gradient)

    if image_letter is not None:
        update_fields.append('image_letter = ?')
        values.append(image_letter)

    update_fields.append('updated_at = CURRENT_TIMESTAMP')
    values.append(article_id)

    sql = f'''
        UPDATE portfolio_articles
        SET {', '.join(update_fields)}
        WHERE id = ?
    '''

    cursor.execute(sql, values)

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected > 0

def delete_article(article_id: int) -> bool:
    """Delete a portfolio article."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM portfolio_articles WHERE id = ?', (article_id,))

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected > 0

if __name__ == '__main__':
    init_db()
