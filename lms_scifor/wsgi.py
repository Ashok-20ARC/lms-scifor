"""
WSGI config for lms_scifor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
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
application = get_wsgi_application()
