"""
Database models for the accounting application.

Contains models for:
- Custom User authentication
- Messaging and consulting services
- Service offerings
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django_otp.plugins.otp_totp.models import TOTPDevice


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    about = models.TextField(blank=True)
    TWO_FACTOR_CHOICES = [
        ('sms', 'ارسال کد via SMS'),
        ('totp', 'برنامه احراز هویت (Google Authenticator)'),
        ('none', 'غیرفعال'),
    ]
    two_factor_method = models.CharField(
        max_length=10,
        choices=TWO_FACTOR_CHOICES,
        default='none'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # برای ذخیره شماره تلفن
    social_avatar = models.URLField(blank=True, null=True)
    social_profile_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.get_full_name()
       
    def get_2fa_devices(self):
        return TOTPDevice.objects.filter(user=self, confirmed=True)
    
    def get_two_factor_method_display(self):
        return dict(self.TWO_FACTOR_CHOICES).get(self.two_factor_method, 'ناشناخته')
    
    def has_2fa_enabled(self):
        return self.two_factor_method != 'none'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        elif self.social_avatar:
            return self.social_avatar
        return '/static/images/default-avatar.png'


class MessagingModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField(_("message"), blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.phone_number}: {self.message}"


class ConsultingModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.phone_number}"


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان خدمت")
    description = models.TextField(verbose_name="توضیحات کوتاه")
    image = models.ImageField(upload_to="services/", verbose_name="تصویر خدمت")
    icon_class = models.CharField(max_length=50, verbose_name="کلاس آیکون (flaticon)", 
                                default="flaticon-profit")
    detailed_description = models.TextField(verbose_name="توضیحات کامل", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    detail_page_url = models.CharField(max_length=200, verbose_name="لینک صفحه جزئیات", 
                                     blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به روز رسانی")

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_detail_url(self):
        if self.detail_page_url:
            return self.detail_page_url
        return reverse('error_404')
