"""
Models for the app_accounting application.

Defines custom user and models for messaging and consulting interactions.
"""

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    about = models.TextField(blank=True)

    def __str__(self):
        """
        Returns the full name of the user.
        """
        return self.get_full_name()


class MessagingModel(models.Model):
    """
    Model representing user messages.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    your_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Returns a readable string representation of the message.
        """
        return f"{self.name} ({self.email}) - {self.phone_number}: {self.your_comment}"


class ConsultingModel(models.Model):
    """
    Model representing user consulting requests.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        """
        Returns a readable string representation of the consulting request.
        """
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
