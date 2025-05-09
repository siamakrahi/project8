"""
Custom middleware classes for authentication and internationalization.

Contains:
- Login attempt rate limiting
- Language preference handling
"""

import logging
from django.core.cache import cache
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class LoginAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_limit = getattr(settings, 'LOGIN_ATTEMPTS_LIMIT', 5)
        self.login_timeout = getattr(settings, 'LOGIN_ATTEMPTS_TIMEOUT', 300)

    def __call__(self, request):
        if request.path == '/signin/' and request.method == 'POST':
            ip = self._get_client_ip(request)
            username = request.POST.get('username', '')
            cache_key = f'login_attempts:{ip}:{username}'
            
            attempts = cache.get(cache_key, 0)
            if attempts >= self.login_limit:
                messages.error(request, _("حساب شما به دلیل تلاش‌های ناموفق متعدد موقتاً مسدود شده است. لطفاً بعداً تلاش کنید."))
                return redirect('signin')
            
            response = self.get_response(request)
            
            if not request.user.is_authenticated:
                attempts += 1
                cache.set(cache_key, attempts, self.login_timeout)
                remaining = self.login_limit - attempts
                if remaining > 0:
                    messages.warning(request, _(f"نام کاربری یا رمز عبور نادرست است. شما {remaining} تلاش باقی مانده دارید."))
            else:
                cache.delete(cache_key)
            
            return response
        
        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = (
            request.GET.get('lang') or
            request.session.get('django_language') or 
            request.COOKIES.get('django_language') or
            request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:2] or
            settings.LANGUAGE_CODE
        )
        
        language = language if language in [lang[0] for lang in settings.LANGUAGES] else settings.LANGUAGE_CODE
        
        translation.activate(language)
        request.LANGUAGE_CODE = language
        request.session['django_language'] = language

