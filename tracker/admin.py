from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display    = ['name', 'serial_number', 'location', 'next_due_date', 'status', 'critical', 'overdue_badge']
    list_filter     = ['status', 'condition', 'critical']
    search_fields   = ['name', 'serial_number', 'location']
    ordering        = ['next_due_date']
    readonly_fields = ['created_at', 'updated_at']

    @admin.display(description='Service Status', ordering='next_due_date')
    def overdue_badge(self, obj):
        if not obj.next_due_date:
            return '—'
        days = (obj.next_due_date - timezone.now().date()).days
        if days < 0:
            return format_html('<span style="color:#b91c1c;font-weight:600;">⚠ {} days overdue</span>', abs(days))
        if days <= 14:
            return format_html('<span style="color:#b45309;font-weight:600;">Due in {} days</span>', days)
        return format_html('<span style="color:#15803d;">On track</span>')
