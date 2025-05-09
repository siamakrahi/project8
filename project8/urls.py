"""
URL configuration for project8.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# Main URL patterns for the project
urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    
    # Include accounting app URLs at root
    path("", include("app_accounting.urls")),
    
    # Include chatbot app URLs under /chatbot/
    path("chatbot/", include("app_chatbot.urls")),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include


# urlpatterns =[
#     path('admin/', admin.site.urls),
#     path('', include('app_accounting.urls')),
#     path('chatbot/', include('app_chatbot.urls')),
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
