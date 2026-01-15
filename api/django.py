import os
import sys
from pathlib import Path

# Ensure the Django project package is on the path
ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / 'myproject'
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Configure settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Use Django ASGI application for Vercel Python runtime
from django.core.asgi import get_asgi_application
app = get_asgi_application()
