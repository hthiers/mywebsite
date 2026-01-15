# Contact Form Setup Guide

The contact form is now fully implemented with email notifications and database backup.

## Features

✅ **Email Notifications** - Get instant email alerts when someone submits the form
✅ **Database Backup** - All messages are saved to the database
✅ **Form Validation** - Client and server-side validation
✅ **Bilingual Support** - Success messages in Spanish and English
✅ **User Feedback** - Visual alerts for success/error states
✅ **Spam Protection** - Basic validation (can add more later)

## How It Works

1. User fills out the form (name, email, message)
2. JavaScript sends data to `/api/contact` endpoint
3. Server validates the data
4. Message is saved to `contact_messages` table in database
5. Email notification is sent to your email
6. User sees success message

## Email Configuration

### Option 1: Gmail (Recommended for testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Portfolio Website"
   - Copy the 16-character password

3. **Add to .env file**:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
MAIL_RECIPIENT=hernanthiers@gmail.com
```

### Option 2: SendGrid (Recommended for production)

SendGrid is a professional email service with better deliverability.

1. **Sign up**: https://sendgrid.com (Free: 100 emails/day)
2. **Create API Key**:
   - Settings → API Keys → Create API Key
   - Give it "Mail Send" permissions
   - Copy the API key

3. **Add to .env file**:
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
MAIL_RECIPIENT=hernanthiers@gmail.com
```

### Option 3: Custom SMTP Server

If you have your own email server:

```env
MAIL_SERVER=mail.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=contact@yourdomain.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=contact@yourdomain.com
MAIL_RECIPIENT=hernanthiers@gmail.com
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask-Mail==0.9.1 along with other dependencies.

### 2. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env
```

Add your email configuration (see options above).

### 3. Initialize Database

The `contact_messages` table will be created automatically when you run the app:

```bash
python app.py
```

Or manually:

```bash
python -c "from database import init_db; init_db()"
```

### 4. Test the Form

1. Run your website: `python app.py`
2. Navigate to contact section
3. Fill out the form and submit
4. Check your email for notification
5. Verify message in database

## Database Schema

The `contact_messages` table has the following structure:

```sql
CREATE TABLE contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    read_status BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Viewing Messages

### Option 1: SQLite Browser

```bash
# Install SQLite Browser (macOS)
brew install --cask db-browser-for-sqlite

# Open database
open data/portfolio.db
```

### Option 2: Command Line

```bash
sqlite3 data/portfolio.db "SELECT * FROM contact_messages ORDER BY created_at DESC;"
```

### Option 3: Python Script

```python
from database import get_all_contact_messages

messages = get_all_contact_messages()
for msg in messages:
    print(f"{msg['name']} ({msg['email']})")
    print(f"Message: {msg['message']}")
    print(f"Received: {msg['created_at']}")
    print("---")
```

### Option 4: Future Admin Panel (Coming Soon)

We can add a messages viewer to the admin panel where you can:
- View all contact messages
- Mark messages as read
- Delete spam messages
- Reply directly from admin panel

## Troubleshooting

### Email Not Sending

**Check logs**:
```bash
# Run app and check console output
python app.py
```

**Common issues**:

1. **Gmail "Less secure app" error**:
   - Solution: Use App Password (see Gmail setup above)
   - Don't use your regular Gmail password

2. **SMTP Authentication Failed**:
   - Double-check username and password
   - Verify MAIL_SERVER and MAIL_PORT
   - Check if 2FA is enabled (requires app password)

3. **Connection Timeout**:
   - Check firewall settings
   - Try different port (465 for SSL, 587 for TLS)
   - Verify MAIL_USE_TLS and MAIL_USE_SSL settings

4. **Email goes to spam**:
   - Use professional email service (SendGrid, Mailgun)
   - Set up SPF and DKIM records for your domain
   - Use verified sender email

### Form Not Submitting

**Check browser console**:
- Open Developer Tools (F12)
- Check Console tab for errors
- Check Network tab for failed requests

**Common issues**:

1. **400 Bad Request**:
   - Missing required fields
   - Invalid data format

2. **500 Internal Server Error**:
   - Check app.py logs
   - Database connection issue
   - Email configuration error

3. **Network Error**:
   - Flask app not running
   - Wrong port or host
   - CORS issue (shouldn't happen with same origin)

### Messages Not Saving to Database

```bash
# Check if table exists
sqlite3 data/portfolio.db ".schema contact_messages"

# Manually create table if needed
python -c "from database import init_db; init_db()"
```

## Security Considerations

### Current Implementation

✅ Server-side validation
✅ Email credentials in .env (not in code)
✅ Messages stored in database
✅ Basic input sanitization

### Recommended Additions

For production, consider adding:

1. **Rate Limiting**:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/contact', methods=['POST'])
@limiter.limit("5 per hour")  # Max 5 submissions per hour per IP
def api_contact():
    ...
```

2. **CAPTCHA** (reCAPTCHA v3):
```html
<!-- Add to form -->
<script src="https://www.google.com/recaptcha/api.js"></script>
<div class="g-recaptcha" data-sitekey="your-site-key"></div>
```

3. **Honeypot Field** (simple spam protection):
```html
<!-- Hidden field that bots will fill -->
<input type="text" name="website" style="display:none">
```

```python
# Reject if honeypot is filled
if data.get('website'):
    return jsonify({'error': 'Spam detected'}), 400
```

4. **Email Validation**:
```python
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

## Email Templates

### Current Email Format

Plain text email with:
- Sender name and email
- Message content
- Reply-to header (for easy replies)

### Future HTML Template (Optional)

```python
from flask_mail import Message

def send_contact_email(name, email, message_text):
    msg = Message(
        subject=f'New Contact from {name}',
        recipients=[app.config['MAIL_RECIPIENT']],
        html=f'''
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #1e3a5f;">New Contact Form Submission</h2>
                <div style="background: #f9fafb; padding: 20px; border-radius: 8px;">
                    <p><strong>From:</strong> {name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                    <p><strong>Message:</strong></p>
                    <div style="background: white; padding: 15px; border-left: 4px solid #3b82f6;">
                        {message_text}
                    </div>
                </div>
                <p style="color: #6b7280; font-size: 0.9rem;">
                    Sent from your portfolio website
                </p>
            </body>
        </html>
        ''',
        reply_to=email
    )
    mail.send(msg)
```

## Testing

### Local Testing

```bash
# Run the app
python app.py

# Test form submission with curl
curl -X POST http://localhost:5001/api/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","message":"This is a test message from the contact form"}'
```

### Production Testing

1. Submit test message from live website
2. Check email inbox for notification
3. Verify message in database
4. Test with invalid data to check validation

## Docker Configuration

Email settings in Docker:

```yaml
# docker-compose.yml
services:
  web:
    environment:
      - MAIL_SERVER=${MAIL_SERVER}
      - MAIL_PORT=${MAIL_PORT}
      - MAIL_USE_TLS=${MAIL_USE_TLS}
      - MAIL_USERNAME=${MAIL_USERNAME}
      - MAIL_PASSWORD=${MAIL_PASSWORD}
      - MAIL_RECIPIENT=${MAIL_RECIPIENT}
```

## Next Steps

1. **Set up email** (Gmail or SendGrid)
2. **Test locally** to verify everything works
3. **Add to production** environment variables
4. **Monitor** for spam submissions
5. **Optional**: Add admin panel to view messages

## Support

If you need help:
- Check logs: `python app.py` (look for error messages)
- Test email config: Try sending test email with `python -c "from app import mail, Message; ..."`
- Database issues: Verify table exists with `sqlite3 data/portfolio.db ".tables"`

## Future Enhancements

Potential improvements:
- [ ] Admin panel to view/manage messages
- [ ] Email templates (HTML formatting)
- [ ] Auto-reply to sender
- [ ] CAPTCHA integration
- [ ] File attachments
- [ ] Message categories/tags
- [ ] Export messages to CSV
- [ ] Email notifications with filters
