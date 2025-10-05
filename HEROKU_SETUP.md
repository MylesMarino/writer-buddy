# Heroku Deployment for third-south-capital

## Step 1: Verify Your Heroku Account
Visit: https://heroku.com/verify and add payment information (free tier won't charge).

## Step 2: Create Heroku App
```bash
cd /Users/myles/Documents/GitHub/writer-buddy
heroku create third-south-capital
```

## Step 3: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:essential-0 -a third-south-capital
```

## Step 4: Add Redis for WebSockets
```bash
heroku addons:create heroku-redis:mini -a third-south-capital
```

## Step 5: Generate and Set Environment Variables
```bash
# Generate a secure secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set config vars (replace YOUR_GENERATED_KEY with output from above)
heroku config:set SECRET_KEY="YOUR_GENERATED_KEY" -a third-south-capital
heroku config:set DEBUG=False -a third-south-capital
heroku config:set ALLOWED_HOSTS="third-south-capital.herokuapp.com" -a third-south-capital
heroku config:set CSRF_TRUSTED_ORIGINS="https://third-south-capital.herokuapp.com" -a third-south-capital
```

## Step 6: Deploy to Heroku
```bash
git push heroku main
```

## Step 7: Run Database Migrations
```bash
heroku run python manage.py migrate -a third-south-capital
```

## Step 8: Create Admin User
```bash
heroku run python manage.py createsuperuser -a third-south-capital
```

## Step 9: Load Writing Rules (Optional)
```bash
heroku run python manage.py add_writing_rules -a third-south-capital
```

## Step 10: Open Your App
```bash
heroku open -a third-south-capital
```

Your app will be available at: **https://third-south-capital.herokuapp.com**

---

## Additional Commands

### View Logs
```bash
heroku logs --tail -a third-south-capital
```

### Check App Info
```bash
heroku info -a third-south-capital
```

### Check Database Info
```bash
heroku pg:info -a third-south-capital
```

### Check Redis Info
```bash
heroku redis:info -a third-south-capital
```

### Restart App
```bash
heroku restart -a third-south-capital
```

### Run Django Shell
```bash
heroku run python manage.py shell -a third-south-capital
```

### Scale Dynos
```bash
heroku ps:scale web=1 -a third-south-capital
```

---

## Troubleshooting

### If deployment fails
1. Check logs: `heroku logs --tail -a third-south-capital`
2. Verify config vars: `heroku config -a third-south-capital`
3. Check build logs: `heroku builds -a third-south-capital`

### If WebSockets don't work
1. Ensure Redis is provisioned: `heroku addons -a third-south-capital`
2. Check Redis URL: `heroku config:get REDIS_URL -a third-south-capital`
3. Restart app: `heroku restart -a third-south-capital`

### If static files don't load
```bash
heroku run python manage.py collectstatic --noinput -a third-south-capital
```

---

## After Deployment

1. Visit: https://third-south-capital.herokuapp.com
2. Create your first document
3. Test real-time collaboration by opening in two browser tabs
4. Share documents using the Share button

Admin panel: https://third-south-capital.herokuapp.com/admin
