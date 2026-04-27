# Deployment Guide

This guide covers multiple deployment options for the MMSU Medical Dashboard.

## Table of Contents
- [Local Development](#local-development)
- [Deploy to Render (Recommended - Free)](#deploy-to-render)
- [Deploy to PythonAnywhere (Free)](#deploy-to-pythonanywhere)
- [Deploy to Heroku](#deploy-to-heroku)
- [Deploy to Railway](#deploy-to-railway)
- [Security Checklist](#security-checklist)

---

## Local Development

1. **Install Python 3.8+** if not already installed
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python app.py
   ```
4. **Access at:** http://127.0.0.1:5000

---

## Deploy to Render (Recommended - Free)

Render offers free hosting with automatic deployments from GitHub.

### Step 1: Prepare Your Repository

1. Create a GitHub account if you don't have one
2. Create a new repository (e.g., `mmsu-medical-dashboard`)
3. Upload all your project files

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `mmsu-medical-dashboard`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

5. Add Environment Variables:
   - Click **"Advanced"** → **"Add Environment Variable"**
   - Add these variables:
     ```
     FLASK_ENV = production
     SECRET_KEY = (generate a random string)
     ADMIN_USERNAME = your_username
     ADMIN_PASSWORD = your_secure_password
     ```

6. Click **"Create Web Service"**
7. Wait for deployment (usually 2-5 minutes)
8. Your app will be live at `https://your-app-name.onrender.com`

**Note:** Free tier sleeps after 15 minutes of inactivity. First request may be slow.

---

## Deploy to PythonAnywhere (Free)

### Step 1: Sign Up

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free "Beginner" account

### Step 2: Upload Files

1. Go to **Files** tab
2. Upload all your project files to `/home/yourusername/mmsu`

### Step 3: Create Web App

1. Go to **Web** tab → **Add a new web app**
2. Choose **Flask** and **Python 3.10**
3. Set path to: `/home/yourusername/mmsu/app.py`

### Step 4: Configure Virtual Environment

1. Open a **Bash console**
2. Run:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 mmsu-env
   pip install -r requirements.txt
   ```

### Step 5: Configure WSGI File

1. Go to **Web** tab
2. Click on WSGI configuration file
3. Replace content with:
   ```python
   import sys
   path = '/home/yourusername/mmsu'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

### Step 6: Set Environment Variables

1. In the WSGI file, add at the top:
   ```python
   import os
   os.environ['FLASK_ENV'] = 'production'
   os.environ['SECRET_KEY'] = 'your-secret-key'
   os.environ['ADMIN_PASSWORD'] = 'your-password'
   ```

### Step 7: Reload

1. Click **Reload** button on the Web tab
2. Your app will be at `yourusername.pythonanywhere.com`

---

## Deploy to Heroku

### Prerequisites

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a Heroku account

### Steps

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Create app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set ADMIN_USERNAME=admin
   heroku config:set ADMIN_PASSWORD="your-password"
   ```

4. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open app:**
   ```bash
   heroku open
   ```

---

## Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Python and deploys
6. Add environment variables in **Variables** tab:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   ADMIN_PASSWORD=your-password
   ```
7. Your app will be at `your-app.up.railway.app`

---

## Security Checklist

Before deploying to production:

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Restrict database access
- [ ] Add rate limiting for login attempts
- [ ] Regular backups of database
- [ ] Monitor application logs
- [ ] Keep dependencies updated

---

## Troubleshooting

### App won't start
- Check all environment variables are set
- Verify Python version (3.8+)
- Check logs for error messages

### Database errors
- Ensure write permissions for `mmsu.db`
- Check database file exists and is not corrupted

### Static files not loading
- Verify file paths are correct
- Check web server configuration

### Login not working
- Verify environment variables are set correctly
- Check browser console for errors
- Clear browser cache and cookies

---

## Support

For issues:
1. Check deployment platform documentation
2. Review application logs
3. Verify all environment variables are set
4. Test locally first

---

**Good luck with your deployment! 🚀**
