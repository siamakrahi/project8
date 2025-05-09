"""
URL configuration for chatbot application.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
]
