"""
Migration script to add image_url support to portfolio articles.
Adds image_url column to store external image URLs.
"""
import sqlite3

DATABASE = 'portfolio.db'

def add_image_url_column():
    """Add image_url column to portfolio_articles table."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Adding image_url support to portfolio articles...")

    # Check if column already exists
    cursor.execute("PRAGMA table_info(portfolio_articles)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'image_url' not in columns:
        print("Adding image_url column...")
        cursor.execute('''
            ALTER TABLE portfolio_articles
            ADD COLUMN image_url TEXT
        ''')
        print("✓ Added image_url column")
    else:
        print("✓ image_url column already exists")

    conn.commit()
    conn.close()

    print("\nMigration completed successfully!")
    print("You can now add image URLs to your portfolio articles.")
    print("\nNote: Articles without image_url will continue to show gradient backgrounds.")

if __name__ == '__main__':
    add_image_url_column()
