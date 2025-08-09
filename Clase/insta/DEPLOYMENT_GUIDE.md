# Django Instagram Clone - Render Deployment Guide

## Overview
This guide will help you deploy your Django Instagram clone to Render.com

## Prerequisites
- GitHub account
- Render account (free tier available)
- Your project pushed to GitHub

## Step 1: Prepare Your Project

### Files Created/Updated:
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `insta/settings.py` - Production-ready configuration
- ✅ `build.sh` - Build script for Render
- ✅ `Procfile` - Process configuration
- ✅ `render.yaml` - Render deployment configuration
- ✅ `.env.example` - Environment variables template

## Step 2: Push to GitHub

```bash
# Navigate to your project directory
cd Clase/insta

# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Render deployment"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

### Method 1: Using Render Dashboard (Recommended)

1. **Create Web Service:**
   - Go to [https://render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select your Django Instagram project

2. **Configure Service:**
   - **Name**: `django-insta-clone`
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn insta.wsgi:application`
   - **Instance Type**: Free (or Starter for better performance)

3. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a new secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `CSRF_TRUSTED_ORIGINS`: `https://your-app.onrender.com`

4. **Create PostgreSQL Database:**
   - Go to "New" → "PostgreSQL"
   - **Name**: `insta-db`
   - **Database**: `insta_db`
   - **User**: `insta_user`
   - **Plan**: Free (or Starter)

5. **Connect Database:**
   - Copy the "Internal Database URL"
   - Add as `DATABASE_URL` environment variable

### Method 2: Using render.yaml (Blueprints)

1. **Push render.yaml to GitHub**
2. **Go to Render Dashboard**
3. **Click "New" → "Blueprint"**
4. **Connect your GitHub repository**
5. **Render will automatically detect render.yaml and deploy**

## Step 4: Post-Deployment

### Create Superuser
After deployment, create a superuser to access Django admin:
```bash
# In Render dashboard, go to your web service
# Click "Shell" tab
python manage.py createsuperuser
```

### Access Your App
- **Main App**: `https://your-app.onrender.com`
- **Admin Panel**: `https://your-app.onrender.com/admin`

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate new |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection | From Render |
| `CSRF_TRUSTED_ORIGINS` | CSRF origins | `https://your-app.onrender.com` |

## Troubleshooting

### Common Issues:

1. **Build fails**: Check build.sh permissions and content
2. **Static files not loading**: Ensure WhiteNoise is configured
3. **Database connection**: Verify DATABASE_URL format
4. **CSRF errors**: Check CSRF_TRUSTED_ORIGINS

### Debug Commands:
```bash
# Check logs in Render dashboard
# Or use shell:
python manage.py check --deploy
python manage.py collectstatic --dry-run
```

## Local Development vs Production

### Local Development:
- Uses SQLite
- DEBUG=True
- Local file storage

### Production:
- Uses PostgreSQL
- DEBUG=False
- Static files served by WhiteNoise
- Media files handled by cloud storage (recommended)

## Next Steps

1. **Set up media file storage** (AWS S3, Cloudinary, etc.)
2. **Configure email backend** (SendGrid, AWS SES)
3. **Set up custom domain**
4. **Enable HTTPS redirect**
5. **Add monitoring and logging**

## Support

If you encounter issues:
- Check Render logs
- Verify all environment variables
- Ensure all migrations are applied
- Check database connectivity
