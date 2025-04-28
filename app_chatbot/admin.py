from django.contrib import admin
from .models import FAQCategory, FAQ

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'truncated_answer', 'category', 'created_at')
    search_fields = ('question', 'answer', 'keywords')
    list_filter = ('category',)
    ordering = ('-created_at',)
    
    def truncated_answer(self, obj):
        return obj.answer[:50] + '...' if len(obj.answer) > 50 else obj.answer
    truncated_answer.short_description = 'پاسخ کوتاه'

admin.site.register(FAQCategory)
admin.site.register(FAQ, FAQAdmin)