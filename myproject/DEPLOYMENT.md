# Deployment Guide

## Production Configuration

Before deploying to production, update `myproject/settings.py`:

### 1. Security Settings

```python
# Set DEBUG to False
DEBUG = False

# Set allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Generate a new SECRET_KEY (keep it secret!)
SECRET_KEY = 'your-secure-random-secret-key-here'

# Enable security features
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 2. Static Files

```python
# Collect static files for production
python manage.py collectstatic
```

### 3. Database

For production, consider using PostgreSQL instead of SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jobsdb',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Environment Variables

Use environment variables for sensitive data:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Generate new SECRET_KEY
- [ ] Enable SSL/HTTPS security settings
- [ ] Configure production database
- [ ] Run collectstatic
- [ ] Set up proper logging
- [ ] Configure email backend for notifications
- [ ] Set up backup strategy
- [ ] Configure CORS if needed
- [ ] Set up monitoring/error tracking

## Development vs Production

**Development** (current state):
- DEBUG = True
- SQLite database
- Development server (`runserver`)
- All features work locally

**Production** (deployment):
- DEBUG = False
- PostgreSQL/MySQL database
- WSGI server (Gunicorn/uWSGI)
- Nginx/Apache reverse proxy
- SSL/HTTPS enabled

## Notes

This project is currently configured for development. The security warnings shown by `manage.py check --deploy` are expected for a development environment and should be addressed before production deployment.
