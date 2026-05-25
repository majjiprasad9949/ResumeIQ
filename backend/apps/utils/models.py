"""
Utility models for system-wide functionality.
"""

from django.db import models


class SystemLog(models.Model):
    """
    System-wide logging for debugging and monitoring.
    """
    LOG_LEVEL_CHOICES = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    level = models.CharField(max_length=20, choices=LOG_LEVEL_CHOICES)
    module = models.CharField(max_length=255)
    message = models.TextField()
    user_id = models.IntegerField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'System Log'
        verbose_name_plural = 'System Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['level']),
        ]
    
    def __str__(self):
        return f"{self.level} - {self.module}"


class AuditLog(models.Model):
    """
    Audit logging for user actions and sensitive operations.
    """
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('download', 'Download'),
        ('upload', 'Upload'),
    ]
    
    user_id = models.IntegerField()
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=255)
    resource_id = models.IntegerField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.resource_type}"


class SystemMetric(models.Model):
    """
    System performance metrics for monitoring.
    """
    METRIC_TYPE_CHOICES = [
        ('api_response_time', 'API Response Time'),
        ('database_query_time', 'Database Query Time'),
        ('cpu_usage', 'CPU Usage'),
        ('memory_usage', 'Memory Usage'),
        ('disk_usage', 'Disk Usage'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPE_CHOICES)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'System Metric'
        verbose_name_plural = 'System Metrics'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['metric_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.metric_type}: {self.value} {self.unit}"
