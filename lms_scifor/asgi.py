"""
ASGI config for lms_scifor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
<<<<<<< HEAD
import sys
import logging
from django.core.asgi import get_asgi_application

# Optional: Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_scifor.settings')

# Optional: Basic logging for ASGI startup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting ASGI application...")

# Initialize ASGI application
application = get_asgi_application()

=======

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_scifor.settings')

application = get_asgi_application()
>>>>>>> 35b384cf718cf4f5eaed9d1bf3a70e71aec60e85
