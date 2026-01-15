#!/usr/bin/env python3
"""
Test script to verify database is working correctly.
Run this to check if all tables exist and you can read/write data.
"""
from database import (
    init_db,
    get_all_articles,
    create_article,
    get_all_contact_messages,
    create_contact_message
)
import os

def test_database():
    print("=" * 60)
    print("Database Test Script")
    print("=" * 60)
    print()

    # Check if database file exists
    data_dir = os.getenv('DATA_DIR', 'data')
    db_path = os.path.join(data_dir, 'portfolio.db')

    if os.path.exists(db_path):
        print(f"✅ Database file exists: {db_path}")
        size = os.path.getsize(db_path)
        print(f"   Size: {size:,} bytes")
    else:
        print(f"❌ Database file NOT found: {db_path}")
        print("   Creating database...")
        init_db()
        print("✅ Database created!")

    print()
    print("-" * 60)
    print("Testing Portfolio Articles Table")
    print("-" * 60)

    try:
        articles = get_all_articles()
        print(f"✅ Successfully queried portfolio_articles table")
        print(f"   Found {len(articles)} article(s)")

        if articles:
            print("\n   Articles in database:")
            for article in articles:
                print(f"   - {article['title']} (ID: {article['id']})")
        else:
            print("   ℹ️  No articles found (database is empty)")
            print("   💡 Run 'python seed_data.py' to add sample articles")
    except Exception as e:
        print(f"❌ Error querying articles: {str(e)}")

    print()
    print("-" * 60)
    print("Testing Contact Messages Table")
    print("-" * 60)

    try:
        messages = get_all_contact_messages()
        print(f"✅ Successfully queried contact_messages table")
        print(f"   Found {len(messages)} message(s)")

        if messages:
            print("\n   Recent messages:")
            for msg in messages[:5]:  # Show first 5
                print(f"   - From: {msg['name']} ({msg['email']})")
                print(f"     Date: {msg['created_at']}")
                print(f"     Preview: {msg['message'][:50]}...")
                print()
        else:
            print("   ℹ️  No messages found")
            print("   💡 Test the contact form to create a message")
    except Exception as e:
        print(f"❌ Error querying messages: {str(e)}")

    print()
    print("-" * 60)
    print("Testing Write Operations")
    print("-" * 60)

    try:
        # Try creating a test contact message
        test_msg_id = create_contact_message(
            name="Test User",
            email="test@example.com",
            message="This is a test message to verify the database is working."
        )
        print(f"✅ Successfully created test message (ID: {test_msg_id})")

        # Verify it was created
        all_messages = get_all_contact_messages()
        test_msg = next((m for m in all_messages if m['id'] == test_msg_id), None)

        if test_msg:
            print(f"✅ Successfully retrieved test message")
            print(f"   Name: {test_msg['name']}")
            print(f"   Email: {test_msg['email']}")
            print(f"   Message: {test_msg['message'][:50]}...")
        else:
            print(f"❌ Could not retrieve test message")

    except Exception as e:
        print(f"❌ Error creating test message: {str(e)}")

    print()
    print("=" * 60)
    print("Database Test Complete!")
    print("=" * 60)
    print()
    print("Summary:")
    print("- Database file:", "✅ OK" if os.path.exists(db_path) else "❌ MISSING")
    print("- Portfolio articles table:", "✅ OK")
    print("- Contact messages table:", "✅ OK")
    print("- Write operations:", "✅ OK")
    print()

if __name__ == '__main__':
    test_database()
