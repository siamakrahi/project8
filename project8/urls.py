"""
URL configuration for project8.

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('app_chatbot.urls')),
    path('', include('app_accounting.urls')),
]
