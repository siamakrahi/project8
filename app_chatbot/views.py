"""
Chatbot view handlers.
"""

from django.shortcuts import render


def chat_view(request):
    """Render the main chat interface."""
    return render(request, 'app_chatbot/chat_widget.html')