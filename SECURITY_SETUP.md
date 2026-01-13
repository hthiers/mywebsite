# Security Setup Guide

This guide explains how to secure your admin panel before deploying to production.

## 🔒 Authentication System

The website now includes a secure authentication system that protects:
- `/admin` - Admin panel interface
- `/api/articles` (POST) - Create articles
- `/api/articles/<id>` (PUT) - Update articles
- `/api/articles/<id>` (DELETE) - Delete articles

Public routes (no authentication required):
- `/` - Main website
- `/api/articles` (GET) - Read articles (for the public website)

## 📋 Setup Instructions

### 1. Generate a Secret Key

Generate a strong secret key for Flask sessions:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Generate Password Hash

Run the password hash generator script:

```bash
python generate_password_hash.py
```

This will prompt you to enter your admin password and generate a secure hash.

### 3. Create .env File

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
SECRET_KEY=your-generated-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your-generated-password-hash-here
```

### 4. Verify .env is in .gitignore

**IMPORTANT**: Make sure `.env` is listed in your `.gitignore` file to prevent committing sensitive credentials to version control.

The `.gitignore` already includes `.env` files.

## 🚀 Production Deployment

### Environment Variables

When deploying to production (e.g., Google Cloud Run, AWS, Heroku), set these environment variables in your hosting platform:

1. `SECRET_KEY` - Your generated secret key
2. `ADMIN_USERNAME` - Your admin username
3. `ADMIN_PASSWORD_HASH` - Your generated password hash

**Never commit these values to Git!**

### Default Credentials (Development Only)

For development/testing purposes, the app uses default credentials if `.env` is not configured:

- **Username**: `admin`
- **Password**: `changeme`

**⚠️ IMPORTANT**: These defaults are for development only. Always set custom credentials in production!

## 🔐 Security Features

1. **Password Hashing**: Passwords are hashed using Werkzeug's `generate_password_hash()` with PBKDF2 SHA-256
2. **Session Management**: Flask sessions with secure secret key
3. **Protected Routes**: Login required decorator on all admin and modification endpoints
4. **HTTPS Recommended**: Always use HTTPS in production to encrypt credentials in transit

## 📝 Usage

### Logging In

1. Navigate to `/login`
2. Enter your admin username and password
3. You'll be redirected to the admin panel

### Logging Out

Click the "Logout" button in the admin panel header, or navigate to `/logout`

## 🛡️ Best Practices

1. **Use Strong Passwords**: Use a password manager to generate strong, unique passwords
2. **Keep .env Secure**: Never commit `.env` to version control
3. **Rotate Credentials**: Change your password periodically
4. **Use HTTPS**: Always use HTTPS in production
5. **Monitor Access**: Check your application logs for unauthorized access attempts

## 🔄 Changing Your Password

1. Generate a new password hash:
   ```bash
   python generate_password_hash.py
   ```

2. Update `ADMIN_PASSWORD_HASH` in your `.env` file (or production environment variables)

3. Restart your application

## 🆘 Troubleshooting

### "Invalid username or password"

- Verify your credentials in the `.env` file
- Ensure the password hash was generated correctly
- Check that the `.env` file is being loaded (run `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('ADMIN_USERNAME'))"`)

### Session Issues

- Make sure `SECRET_KEY` is set in your `.env` file
- Verify cookies are enabled in your browser
- Clear your browser cookies for the site

### Locked Out

If you lose access:

1. Generate a new password hash
2. Update your `.env` file with the new hash
3. Restart the application
