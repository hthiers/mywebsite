#!/usr/bin/env python3
"""
Generate a secure password hash for the admin user.
Run this script to create a hash for your admin password.
"""
from werkzeug.security import generate_password_hash
import getpass

def main():
    print("=" * 50)
    print("Admin Password Hash Generator")
    print("=" * 50)
    print("\nThis script will generate a secure hash for your admin password.")
    print("Copy the generated hash to your .env file as ADMIN_PASSWORD_HASH.\n")

    # Get password from user (hidden input)
    password = getpass.getpass("Enter your admin password: ")
    password_confirm = getpass.getpass("Confirm your admin password: ")

    # Verify passwords match
    if password != password_confirm:
        print("\n❌ Error: Passwords do not match!")
        return

    # Generate hash
    password_hash = generate_password_hash(password)

    print("\n" + "=" * 50)
    print("✅ Password hash generated successfully!")
    print("=" * 50)
    print("\nAdd this to your .env file:")
    print(f"\nADMIN_PASSWORD_HASH={password_hash}")
    print("\n" + "=" * 50)
    print("⚠️  Keep this hash secure and never share it publicly!")
    print("=" * 50)

if __name__ == '__main__':
    main()
