"""
ASGI config for project8.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://channels.readthedocs.io/en/stable/deploying.html
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project8.settings")

# Initialize Django
django.setup()

# Import WebSocket routing after Django setup
import app_chatbot.routing

# ASGI application routing
application = ProtocolTypeRouter({
    # Standard HTTP requests
    "http": get_asgi_application(),
    
    # WebSocket connections with authentication
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app_chatbot.routing.websocket_urlpatterns
        )
    ),
})
