"""
WSGI config for lms_scifor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
<<<<<<< HEAD
import sys
import logging
from django.core.wsgi import get_wsgi_application

# Optional: Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_scifor.settings')

# Optional: Basic logging for WSGI
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting WSGI application...")

# Get the WSGI application
=======

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_scifor.settings')

>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
application = get_wsgi_application()
