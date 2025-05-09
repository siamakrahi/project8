"""
Views for the accounting application.

This module contains all view functions and classes that handle:
- User authentication (login, logout, registration)
- Two-factor authentication setup and verification
- Messaging and consulting services
- Password reset functionality
- User profile management
- Search functionality
"""

import os
import json
import requests
import qrcode
import qrcode.image.svg
import base64
import random
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model, forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages import constants as message_constants
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.html import strip_tags
from django.db.models import Q
from django.conf import settings
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.forms import OTPTokenForm
from django_otp import devices_for_user, login as otp_login
from otp_twilio.models import TwilioSMSDevice as SMSDevice
from io import BytesIO
from django_ratelimit.decorators import ratelimit
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.urls import reverse_lazy
from .models import User, MessagingModel, ConsultingModel, Service
from .forms import CustomUserCreationForm, MessagingForm, ConsultingForm, CustomPasswordResetForm, ProfileForm
from .forms import TwoFactorMethodForm
from .forms import CustomPasswordResetForm


# ======================
# STATIC PAGES
# ======================

def home(request):
    return render(request, "app_accounting/home.html")


def service(request):
    return render(request, "app_accounting/service.html")


def team(request):
    return render(request, "app_accounting/team.html")


def contact(request):
    return render(request, "app_accounting/contact.html")


def error_404(request):
    return render(request, "app_accounting/error_404.html", status=404)


# ======================
# USER AUTHENTICATION
# ======================

def signin_view(request):
    if request.method == "POST":
        form = auth_forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.has_2fa_enabled():
                request.session['2fa_user_id'] = user.id
                request.session['2fa_verified'] = False
                return redirect('verify_2fa')

            login(request, user)
            messages.success(request, "ورود موفقیت‌آمیز بود!")
            return redirect("home")
        else:
            messages.error(request, "نام کاربری یا رمز عبور نادرست است.")
    else:
        form = auth_forms.AuthenticationForm()

    return render(request, 'app_accounting/signin.html', {'form': form})


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            messages.success(request, "حساب کاربری شما با موفقیت ایجاد شد!")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "app_accounting/signup.html", {"form": form})

def signout_view(request):
    logout(request)
    return redirect("home")


# ======================
# TWO-FACTOR AUTHENTICATION
# ======================

@login_required
def setup_2fa(request):
    if request.method == 'POST':
        form = TwoFactorMethodForm(request.POST)
        if form.is_valid():
            request.user.two_factor_method = form.cleaned_data['method']

            if form.cleaned_data['method'] == 'sms':
                request.user.phone_number = form.cleaned_data['phone_number']
                request.user.save()

                device = SMSDevice.objects.create(
                    user=request.user,
                    name='SMS',
                    number=request.user.phone_number,
                    key=str(random.randint(100000, 999999))
                )
                device.generate_challenge()
                return redirect('setup_2fa')

            elif form.cleaned_data['method'] == 'totp':
                return redirect('setup_totp')

    else:
        form = TwoFactorMethodForm()

    return render(request, 'app_accounting/choose_2fa_method.html', {'form': form})


@login_required
def setup_totp(request):
    TOTPDevice.objects.filter(user=request.user).delete()

    device = TOTPDevice(user=request.user, confirmed=False)
    device.save()

    qr_code_url = device.config_url
    secret_key = qr_code_url.split('secret=')[1].split('&')[0]

    img = qrcode.make(qr_code_url, image_factory=qrcode.image.svg.SvgImage)
    buffer = BytesIO()
    img.save(buffer)
    qr_code_svg = buffer.getvalue().decode()

    if request.method == 'POST':
        form = OTPTokenForm(user=request.user, data=request.POST)
        if form.is_valid():
            if device.verify_token(form.cleaned_data['otp_token']):
                device.confirmed = True
                device.save()
                request.user.two_factor_method = 'totp'
                request.user.save()
                messages.success(
                    request, "احراز هویت دو مرحله‌ای با موفقیت فعال شد!")
                return redirect('profile')
            else:
                messages.error(request, "کد وارد شده نامعتبر است")
    else:
        form = OTPTokenForm(user=request.user)

    return render(request, 'app_accounting/setup_totp.html', {
        'form': form,
        'qr_code_url': qr_code_url,
        'secret_key': secret_key,
        'qr_code_svg': qr_code_svg
    })


@login_required
def verify_sms(request):
    try:
        device = SMSDevice.objects.get(user=request.user)
    except SMSDevice.DoesNotExist:
        messages.error(request, "دستگاه SMS یافت نشد")
        return redirect('setup_2fa')

    if request.method == 'POST':
        form = OTPTokenForm(user=request.user, data=request.POST)
        if form.is_valid():
            if device.verify_token(form.cleaned_data['otp_token']):
                device.confirmed = True
                device.save()
                request.user.two_factor_method = 'sms'
                request.user.save()
                messages.success(
                    request, "احراز هویت دو مرحله‌ای via SMS فعال شد!")
                return redirect('profile')
            else:
                messages.error(request, "کد وارد شده نامعتبر است")
    else:
        form = OTPTokenForm(user=request.user)

    return render(request, 'app_accounting/verify_sms.html', {
        'form': form,
        'phone_number': request.user.phone_number
    })


@login_required
def disable_2fa(request):
    if request.method == 'POST':
        TOTPDevice.objects.filter(user=request.user).delete()
        SMSDevice.objects.filter(user=request.user).delete()

        request.user.two_factor_method = 'none'
        request.user.save()

        messages.success(request, "احراز هویت دو مرحله‌ای غیرفعال شد")
        return redirect('profile')

    return render(request, 'app_accounting/disable_2fa.html')


logger = logging.getLogger(__name__)

@login_required
@require_POST
@csrf_exempt
@ratelimit(key='user', rate='3/h', method='POST', block=True)
def resend_sms_code(request):
    try:
        device = SMSDevice.objects.get(user=request.user)
        
        new_code = str(random.randint(100000, 999999))
        device.key = new_code
        device.save()
        
        if not settings.DEBUG:
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'کد تأیید شما برای {settings.SITE_NAME}: {new_code}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=request.user.phone_number
                )
                logger.info(f"SMS sent to {request.user.phone_number}, SID: {message.sid}")
            except TwilioRestException as e:
                logger.error(f"Twilio error for {request.user.phone_number}: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': 'خطا در ارسال پیامک. لطفاً با پشتیبانی تماس بگیرید.'
                }, status=500)
        else:
            logger.debug(f"DEV MODE: SMS code for {request.user.phone_number}: {new_code}")
        
        return JsonResponse({
            'success': True,
            'message': 'کد جدید ارسال شد'
        })

    except SMSDevice.DoesNotExist:
        logger.error(f"SMS device not found for user {request.user.username}")
        return JsonResponse({
            'success': False,
            'message': 'دستگاه SMS یافت نشد. لطفاً روش احراز هویت را مجدداً تنظیم کنید.'
        }, status=404)
    
    except Exception as e:
        logger.critical(f"Unexpected error in resend_sms_code: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'خطای سیستمی. لطفاً بعداً تلاش کنید.'
        }, status=500)


@never_cache
def verify_2fa(request):
    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return redirect('signin')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "کاربر یافت نشد")
        return redirect('signin')

    method = user.two_factor_method

    if request.method == 'POST':
        form = OTPTokenForm(user=user, data=request.POST)
        if form.is_valid():
            device = next(devices_for_user(user), None)
            if device and device.verify_token(form.cleaned_data['otp_token']):
                request.session['2fa_verified'] = True
                login(request, user)
                otp_login(request, device)
                messages.success(request, "احراز هویت با موفقیت انجام شد!")
                return redirect('home')
            messages.error(request, "کد وارد شده نامعتبر است")
    else:
        form = OTPTokenForm(user=user)

    template = 'app_accounting/verify_sms.html' if method == 'sms' else 'app_accounting/verify_totp.html'
    return render(request, template, {
        'form': form,
        'method': method,
        'phone_number': user.phone_number if method == 'sms' else None
    })


# ======================
# MESSAGING & CONSULTING
# ======================

@login_required
def create_messaging(request):
    if request.method == "POST":
        form = MessagingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "پیام شما با موفقیت ارسال شد",
                extra_tags="messaging")
            return redirect("contact")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request,
                    f"{field}: {error}",
                    extra_tags="messaging")

    return redirect("contact")


@login_required
def create_consulting(request):
    if request.method == "POST":
        form = ConsultingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "درخواست مشاوره شما با موفقیت ثبت شد",
                extra_tags="consulting")
            return redirect("contact")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    request,
                    f"{field}: {error}",
                    extra_tags="consulting")

    return redirect("contact")


# ======================
# PASSWORD RESET
# ======================

def password_reset_view(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email__iexact=email)
            
            if users.exists():
                for user in users:
                    send_password_reset_email(request, user)
                return render(request, "registration/custom_password_reset_done.html")
            
            form.add_error('email', 'ایمیل وارد شده در سیستم وجود ندارد')
            return render(request, "registration/password_reset.html", {
                "form": form
            })
    
    return render(request, "registration/password_reset.html", {
        "form": CustomPasswordResetForm()
    })

def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    subject = f"بازنشانی رمز عبور - {current_site.name}"
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(f"/reset/{uid}/{token}/")

    context = {
        "user": user,
        "site_name": current_site.name,
        "reset_url": reset_url,
        "uid": uid,
        "token": token,
    }

    html_message = render_to_string(
        "registration/custom_password_reset_email.html",
        context,
        request=request
    )
    
    text_message = render_to_string(
        "registration/custom_password_reset_email.txt",
        context,
        request=request
    )

    send_mail(
        subject=subject,
        message=text_message,
        from_email=f"noreply@{current_site.domain}",
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False
    )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete.html'


# ======================
# PROFILE MANAGEMENT
# ======================

@login_required
def profile_view(request):
    return render(request, "app_accounting/profile.html",
                  {"user": request.user})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "تغییرات پروفایل با موفقیت ذخیره شد!")
            return redirect("profile")
        messages.error(request, "لطفاً خطاهای فرم را اصلاح کنید.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "app_accounting/edit_profile.html", {"form": form})


# ======================
# SEARCH FUNCTIONALITY
# ======================

def _get_snippet(text, query, max_length=150):
    index = text.lower().find(query.lower())
    if index == -1:
        return ""

    start = max(0, index - 30)
    end = min(len(text), index + len(query) + 120)
    snippet = text[start:end]

    if start > 0:
        snippet = '...' + snippet
    if end < len(text):
        snippet = snippet + '...'

    return snippet

def search_pages(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        searchable_pages = [
            'home.html',
            'service.html',
            'team.html',
            'contact.html',
            'profile.html',
            'edit_profile.html',
            'signin.html',
            'signup.html'
        ]

        templates_dir = os.path.join(settings.BASE_DIR, 'templates', 'app_accounting')

        for page in searchable_pages:
            file_path = os.path.join(templates_dir, page)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    text_content = strip_tags(content)

                    if query.lower() in text_content.lower():
                        results.append({
                            'title': os.path.splitext(page)[0].replace('_', ' ').title(),
                            'url': page.replace('.html', ''),
                            'snippet': _get_snippet(text_content, query)
                        })
            except FileNotFoundError:
                continue

    return render(request, 'app_accounting/search_results.html', {
        'results': results,
        'query': query
    })


# ======================
# SERVICE ADMIN
# ======================

# def service(request):
#     services = Service.objects.filter(is_active=True).order_by('order')
#     context = {
#         'services': services
#     }
#     return render(request, "app_accounting/service.html", context)
