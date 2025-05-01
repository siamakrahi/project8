"""
Admin configuration for the app_accounting application.

Defines custom admin models for User, MessagingModel, and ConsultingModel.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from app_accounting.models import User, MessagingModel, ConsultingModel, Service
from parler.admin import TranslatableAdmin
from app_accounting.models import ServiceTrans

    
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "avatar",
                "about",
            ),
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']


class MessagingAdmin(admin.ModelAdmin):
    title = 'messaging_users'
    list_display = ("id", "email", "phone_number", "your_comment")
    def get_queryset_for_request_user(self, request):
        current_user = request.user
        qs = super().get_queryset(request)
        return qs.filter(user=current_user)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class ConsultingAdmin(admin.ModelAdmin):
    title = 'consulting_users'
    list_display = ("email", "phone_number")
    def get_queryset_for_request_user(self, request):
        current_user = request.user
        qs = super().get_queryset(request)
        return qs.filter(user=current_user)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'short_description', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('icon_preview', 'image_preview', 'created_at', 'updated_at')
    prepopulated_fields = {'detail_page_url': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'detailed_description')
        }),
        ('تصویر و آیکون', {
            'fields': ('image', 'icon_class', 'icon_preview', 'image_preview')
        }),
        ('تنظیمات نمایش', {
            'fields': ('is_active', 'order', 'detail_page_url')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    short_description.short_description = 'توضیحات کوتاه'
    
    def icon_preview(self, obj):
        from django.utils.html import format_html
        return format_html(f'<i class="{obj.icon_class} fa-2x" style="color: #4e73df;"></i> {obj.icon_class}')
    icon_preview.short_description = 'پیش‌نمایش آیکون'
    
    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return "-"
    image_preview.short_description = 'پیش‌نمایش تصویر'


@admin.register(ServiceTrans)
class ServiceTransAdmin(TranslatableAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')


# Register models in admin site
admin.site.register(User, UserAdmin)
admin.site.register(MessagingModel, MessagingAdmin)  
admin.site.register(ConsultingModel, ConsultingAdmin)
