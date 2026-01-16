# WSGI configuration for PythonAnywhere deployment
import os
import sys

# Add project directory to path
path = '/home/YOUR_USERNAME/job-rec-system/myproject'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Set environment variables for production
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', 'YOUR_USERNAME.pythonanywhere.com')

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
