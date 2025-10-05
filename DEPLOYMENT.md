# Writer Buddy - Deployment Guide

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed (`brew install heroku`)
- Git initialized in project

### Step 1: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Create Heroku App
```bash
heroku create your-app-name
```

### Step 3: Add Required Add-ons
```bash
# PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Redis for WebSocket channel layer
heroku addons:create heroku-redis:mini
```

### Step 4: Set Environment Variables
```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set CSRF_TRUSTED_ORIGINS="https://your-app-name.herokuapp.com"
```

### Step 5: Deploy
```bash
git push heroku main
```

### Step 6: Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

### Step 7: Load Writing Rules (Optional)
```bash
heroku run python manage.py add_writing_rules
```

### Step 8: Open Your App
```bash
heroku open
```

---

## Custom Domain Setup

### Add Your Domain
```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```

### Update Environment Variables
```bash
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com,www.yourdomain.com,yourdomain.com"
heroku config:set CSRF_TRUSTED_ORIGINS="https://your-app-name.herokuapp.com,https://www.yourdomain.com,https://yourdomain.com"
```

### Configure DNS
Add the following DNS records to your domain:

**CNAME Record:**
- Name: `www`
- Value: `your-app-name.herokuapp.com`

**ALIAS/ANAME Record** (for root domain):
- Name: `@`
- Value: `your-app-name.herokuapp.com`

---

## Collaboration Features

### WebSocket Support
Real-time collaboration uses WebSockets via Django Channels:
- **Development**: In-memory channel layer (single-process only)
- **Production**: Redis channel layer (multi-process, multi-dyno support)

### Enable Real-time Collaboration
1. Redis is automatically configured via `REDIS_URL` env var (from Heroku Redis add-on)
2. WebSocket connections use `wss://` protocol in production
3. Multiple users can edit the same document simultaneously
4. Cursor positions are shared in real-time (when implemented)

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-abc123...` |
| `DEBUG` | Debug mode (True/False) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `app.herokuapp.com,yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins | `https://app.herokuapp.com` |
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by Heroku |
| `REDIS_URL` | Redis connection string | Auto-set by Heroku |

---

## Monitoring & Logs

### View Logs
```bash
heroku logs --tail
```

### Check App Status
```bash
heroku ps
```

### Restart App
```bash
heroku restart
```

---

## Scaling (Optional)

### Scale Web Dynos
```bash
heroku ps:scale web=2
```

### Upgrade Database
```bash
heroku addons:upgrade heroku-postgresql:basic
```

### Upgrade Redis
```bash
heroku addons:upgrade heroku-redis:premium-0
```

---

## Troubleshooting

### Static Files Not Loading
```bash
heroku run python manage.py collectstatic --noinput
```

### Database Issues
```bash
heroku pg:info
heroku pg:reset DATABASE_URL --confirm your-app-name
heroku run python manage.py migrate
```

### WebSocket Connection Errors
- Ensure Redis add-on is provisioned: `heroku addons`
- Check `REDIS_URL` is set: `heroku config:get REDIS_URL`
- Verify firewall allows WebSocket connections (port 443)

---

## Local Testing with Production Settings

### Create `.env` file
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run with production settings
```bash
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```
