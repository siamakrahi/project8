"""
Chatbot application configuration.
"""

from django.apps import AppConfig


class AppChatbotConfig(AppConfig):
    """Configuration for chatbot application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_chatbot'