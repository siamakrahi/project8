"""
ASGI routing configuration for Channels.

Defines protocol routing for both HTTP and WebSocket connections.
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Import WebSocket URL patterns from chatbot app
import app_chatbot.routing

# Main ASGI application routing
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
