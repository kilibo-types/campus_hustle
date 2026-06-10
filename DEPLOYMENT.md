# Render Deployment Guide

## Prerequisites
- GitHub account (repo already connected)
- Render account (free tier available at https://render.com)

## Step-by-Step Deployment

### 1. Create Render Account & Connect GitHub
1. Visit https://render.com
2. Click "Sign up" → Select "GitHub"
3. Authorize GitHub access

### 2. Create a New Web Service
1. In Render Dashboard, click "New +" → "Web Service"
2. Select your GitHub repository: `kilibo-types/campus_hustle`
3. Choose branch: `main`

### 3. Configure the Service
- **Name**: `campus-hustle` (or your choice)
- **Environment**: `Docker`
- **Plan**: `Starter` (free tier available)
- **Root Directory**: `.` (leave blank)

### 4. Set Environment Variables
In the "Environment" section, add:
- `DJANGO_SECRET_KEY`: Generate a strong secret (e.g., use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DJANGO_DEBUG`: `False`
- `DJANGO_ALLOWED_HOSTS`: Your Render URL (e.g., `campus-hustle.onrender.com`)

### 5. Deploy
- Click "Create Web Service"
- Render will build the Docker image and start the app
- Your app will be available at `https://campus-hustle.onrender.com` (or your chosen name)

## Auto-Deploy on Push
After creating the service, get the Deploy Hook from Render:
1. Go to your service settings → Deploy
2. Copy the "Deploy Hook" URL
3. Add to GitHub Secrets:
   - Go to repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: Paste the hook URL
4. Now every push to `main` will auto-deploy

## Troubleshooting

**Port issues**: Render uses the `$PORT` env var. The Dockerfile is configured to use it.

**Database**: Currently using SQLite. For persistence across deploys, consider adding Render PostgreSQL.

**Static files**: WhiteNoise handles serving static files in production.

## Alternative: Deploy to Railway, Fly.io, or Heroku
Add `Procfile` to repo if needed:
```
web: gunicorn myproject.wsgi:application
```
