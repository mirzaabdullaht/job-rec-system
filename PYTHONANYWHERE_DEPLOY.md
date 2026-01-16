# PythonAnywhere Deployment Guide
# Job Access Recommendation System

## Prerequisites
- GitHub account with repo: https://github.com/mirzaabdullaht/job-rec-system
- PythonAnywhere free account

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account
- Go to https://www.pythonanywhere.com/registration/register/beginner/
- Sign up (completely free, no credit card)
- Confirm your email

### 2. Open Bash Console
- Dashboard → "Consoles" → "Bash"

### 3. Clone Your Repository
```bash
git clone https://github.com/mirzaabdullaht/job-rec-system.git
cd job-rec-system/myproject
```

### 4. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

### 5. Setup Static Files
```bash
python manage.py collectstatic --noinput
```

### 6. Run Database Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Configure Web App
- Dashboard → "Web" → "Add a new web app"
- Choose "Manual configuration"
- Select Python 3.10
- Click through setup

### 9. Configure WSGI File
- In Web tab, click on WSGI configuration file link
- Delete all content and paste from `pythonanywhere_wsgi.py`
- Replace `YOUR_USERNAME` with your PythonAnywhere username (2 places)
- Save file (Ctrl+S or click Save)

### 10. Set Static Files Mapping
In Web tab, scroll to "Static files":
- URL: `/static/`
- Directory: `/home/YOUR_USERNAME/job-rec-system/myproject/static`

### 11. Set Working Directory
In Web tab → "Code" section:
- Source code: `/home/YOUR_USERNAME/job-rec-system/myproject`
- Working directory: `/home/YOUR_USERNAME/job-rec-system/myproject`

### 12. Configure Virtual Environment
In Web tab → "Virtualenv" section:
- Enter path: `/home/YOUR_USERNAME/.virtualenvs/myenv`

### 13. Reload Web App
- Scroll to top of Web tab
- Click green "Reload" button

### 14. Visit Your Site
Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

## Environment Variables (Optional)
If you need to set env vars:
- Go to Web tab → "Environment variables" section
- Add:
  - `DJANGO_SECRET_KEY`: (generate a random string)
  - `DJANGO_DEBUG`: `False`

## Seed Initial Data
In Bash console:
```bash
cd ~/job-rec-system/myproject
python manage.py seed_jobs
```

## Troubleshooting
- **500 Error**: Check error log in Web tab
- **Static files not loading**: Verify static files mapping
- **Database errors**: Re-run migrations
- **Import errors**: Reinstall requirements in virtualenv

## Update After Code Changes
```bash
cd ~/job-rec-system
git pull
cd myproject
python manage.py collectstatic --noinput
python manage.py migrate
# Click Reload in Web tab
```

## Free Tier Limits
- 512 MB disk space
- 1 web app
- MySQL database included
- Good for hobby/student projects
