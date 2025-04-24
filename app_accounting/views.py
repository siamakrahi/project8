"""
Views for the app_accounting application.

Handles user authentication, profile management, messaging, consulting,
password reset, search functionality, and main page rendering.
"""

import os
import json
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model, forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages import constants as message_constants
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from django.db.models import Q
from django.conf import settings
from django.utils.html import strip_tags
from django.http import Http404
from .models import User, MessagingModel, ConsultingModel, Service
from .forms import CustomUserCreationForm, MessagingForm, ConsultingForm, CustomPasswordResetForm, ProfileForm


# Pages:
# -------------------------------------------------------------------------------------------------
def home(request):
    """Render the home page."""
    return render(request, "app_accounting/home.html")

def service(request):
    """Render the service page."""
    return render(request, "app_accounting/service.html")

def team(request):
    """Render the team page."""
    return render(request, "app_accounting/team.html")

def contact(request):
    """Render the contact page."""
    return render(request, "app_accounting/contact.html")

def error_404(request):
    return render(request, "app_accounting/error_404.html", status=404)


# User authentication:
# -------------------------------------------------------------------------------------------------
def signin_view(request):
    """Handle user sign-in."""
    if request.method == "POST":
        form = auth_forms.AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
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
            login(request, user) 
            messages.success(request, "حساب کاربری شما با موفقیت ایجاد شد!")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "app_accounting/signup.html", {"form": form})

def signout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("home")


# Messaging and consulting:
# -------------------------------------------------------------------------------------------------
@login_required
def create_messaging(request):
    """Handle user messaging submissions."""
    if request.method == "POST":
        form = MessagingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد", extra_tags="messaging")  
            return redirect("contact")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}", extra_tags="messaging")
    
    return redirect("contact")

@login_required
def create_consulting(request):
    """Handle user consulting requests."""
    if request.method == "POST":
        form = ConsultingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "درخواست مشاوره شما با موفقیت ثبت شد", extra_tags="consulting")  
            return redirect("contact")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}", extra_tags="consulting")
    
    return redirect("contact")


# Password reset:
# -------------------------------------------------------------------------------------------------
def password_reset_view(request):
    """Handle password reset request."""
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    send_password_reset_email(request, user)
                return render(request, "registration/custom_password_reset_done.html")
            return render(request, "password_reset.html", {
                "form": form,
                "js_alert": "ایمیل واردشده در سیستم وجود ندارد",
            })
    return render(request, "password_reset.html", {"form": CustomPasswordResetForm()})

def send_password_reset_email(request, user):
    """Send password reset email to the user."""
    current_site = get_current_site(request)
    #subject = "بازنشانی رمز عبور - {}".format(current_site.name)
    subject = f"بازنشانی رمز عبور - {current_site.name}"
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # reset_path = "/reset/{}/{}/".format(uid, token)
    # reset_url = request.build_absolute_uri(reset_path)
    reset_url = request.build_absolute_uri(f"/reset/{uid}/{token}/")

    context = {
        "user": user,
        "site_name": current_site.name,
        "reset_url": reset_url,
        "uid": uid,
        "token": token,
    }

    text_message = render_to_string("registration/custom_password_reset_email.txt", context, request=request)
    html_message = render_to_string("registration/custom_password_reset_email.html", context, request=request)

    send_mail(
        subject,
        text_message,
        #'noreply@{}'.format(current_site.domain.split(':')[0]),
        f"noreply@{current_site.domain.split(':')[0]}",
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


# Profile management:
# -------------------------------------------------------------------------------------------------
@login_required
def profile_view(request):
    """Render the user profile page."""
    return render(request, "app_accounting/profile.html", {"user": request.user})

@login_required
def edit_profile(request):
    """Handle user profile editing."""
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


# Search functionality:
# -------------------------------------------------------------------------------------------------
def _get_snippet(text, query, max_length=150):
    index = text.find(query)
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
    query = request.GET.get('q', '').strip().lower()
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
                    text_content = strip_tags(content).lower()
                    
                    if query in text_content:
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
    
# Servie Admin:
# -------------------------------------------------------------------------------------------------
def service(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    context = {
        'services': services
    }
    return render(request, "app_accounting/service.html", context)