"""
WSGI config for project8.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'wsgi' application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project8.settings")

# WSGI application object used by WSGI servers like Gunicorn
application = get_wsgi_application()
