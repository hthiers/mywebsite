"""
Migration script to add language support to portfolio articles.
Adds title_en and description_en columns to the database.
"""
import sqlite3

DATABASE = 'portfolio.db'

def migrate_database():
    """Add language fields to existing database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    print("Starting database migration...")

    # Check if columns already exist
    cursor.execute("PRAGMA table_info(portfolio_articles)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add title_en column if it doesn't exist
    if 'title_en' not in columns:
        print("Adding title_en column...")
        cursor.execute('''
            ALTER TABLE portfolio_articles
            ADD COLUMN title_en TEXT
        ''')
        # Set default English titles (copy from Spanish for now)
        cursor.execute('''
            UPDATE portfolio_articles
            SET title_en = title
            WHERE title_en IS NULL
        ''')
        print("✓ Added title_en column")
    else:
        print("✓ title_en column already exists")

    # Add description_en column if it doesn't exist
    if 'description_en' not in columns:
        print("Adding description_en column...")
        cursor.execute('''
            ALTER TABLE portfolio_articles
            ADD COLUMN description_en TEXT
        ''')
        # Set default English descriptions (copy from Spanish for now)
        cursor.execute('''
            UPDATE portfolio_articles
            SET description_en = description
            WHERE description_en IS NULL
        ''')
        print("✓ Added description_en column")
    else:
        print("✓ description_en column already exists")

    conn.commit()
    conn.close()

    print("\nMigration completed successfully!")
    print("Note: English translations are currently copies of Spanish text.")
    print("You can update them manually or via the API.")

if __name__ == '__main__':
    migrate_database()
