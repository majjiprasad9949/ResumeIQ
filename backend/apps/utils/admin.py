"""
Admin configuration for utils app.
"""

from django.contrib import admin
from .models import SystemLog, AuditLog, SystemMetric


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """Admin for SystemLog model."""
    list_display = ['level', 'module', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['module', 'message']
    readonly_fields = ['created_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model."""
    list_display = ['user_id', 'action', 'resource_type', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user_id', 'resource_type']
    readonly_fields = ['created_at']


@admin.register(SystemMetric)
class SystemMetricAdmin(admin.ModelAdmin):
    """Admin for SystemMetric model."""
    list_display = ['metric_type', 'value', 'unit', 'created_at']
    list_filter = ['metric_type', 'created_at']
    search_fields = ['metric_type']
    readonly_fields = ['created_at']
