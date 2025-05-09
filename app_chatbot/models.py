"""
Database models for chatbot knowledge base.
"""

from django.db import models


class FAQCategory(models.Model):
    """Category for organizing FAQ entries."""
    
    name = models.CharField(max_length=100, verbose_name="Category Name")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon Class")

    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"

    def __str__(self):
        return f"{self.name}"


class FAQ(models.Model):
    """Frequently Asked Question entry with answers."""
    
    question = models.TextField(verbose_name="Question")
    answer = models.TextField(verbose_name="Answer")
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Category"
    )
    keywords = models.TextField(
        blank=True,
        verbose_name="Keywords",
        help_text="Comma-separated list of search keywords"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ Entry"
        verbose_name_plural = "FAQ Entries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.question[:50]}..." if len(self.question) > 50 else self.question


# from django.db import models

# class FAQCategory(models.Model):
#     name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
#     icon = models.CharField(max_length=50, blank=True, verbose_name="آیکن")

#     class Meta:
#         verbose_name = "دسته‌بندی سوالات"
#         verbose_name_plural = "دسته‌بندی‌های سوالات"

#     def __str__(self):
#         return f"{self.name}"

# class FAQ(models.Model):
#     question = models.TextField(verbose_name="سوال")
#     answer = models.TextField(verbose_name="پاسخ")
#     category = models.ForeignKey(
#         FAQCategory, 
#         on_delete=models.SET_NULL, 
#         null=True, 
#         blank=True, 
#         verbose_name="دسته‌بندی"
#     )
#     keywords = models.TextField(blank=True, verbose_name="کلمات کلیدی (با کاما جدا کنید)")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "سوال متداول"
#         verbose_name_plural = "سوالات متداول"

#     def __str__(self):
#         return self.question[:50] + "..."
    