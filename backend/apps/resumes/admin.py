"""
Admin configuration for resumes app.
"""

from django.contrib import admin
from .models import Resume, ResumeVersion, ParsedResume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Admin for Resume model."""
    list_display = ['title', 'user', 'file_format', 'file_size', 'version_number', 'is_current', 'created_at']
    list_filter = ['file_format', 'is_current', 'created_at']
    search_fields = ['title', 'user__email']
    readonly_fields = ['file_size', 'version_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Resume Info', {
            'fields': ('user', 'title', 'file', 'file_format', 'file_size')
        }),
        ('Content', {
            'fields': ('raw_text',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_current', 'version_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ResumeVersion)
class ResumeVersionAdmin(admin.ModelAdmin):
    """Admin for ResumeVersion model."""
    list_display = ['resume', 'version_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['resume__title', 'resume__user__email']
    readonly_fields = ['created_at']


@admin.register(ParsedResume)
class ParsedResumeAdmin(admin.ModelAdmin):
    """Admin for ParsedResume model."""
    list_display = ['resume', 'full_name', 'email', 'parsing_status', 'parsing_confidence', 'created_at']
    list_filter = ['parsing_status', 'created_at']
    search_fields = ['resume__title', 'resume__user__email', 'full_name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'parsing_confidence']
    
    fieldsets = (
        ('Resume', {
            'fields': ('resume',)
        }),
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone', 'location')
        }),
        ('Professional Info', {
            'fields': ('summary',),
            'classes': ('collapse',)
        }),
        ('Extracted Data', {
            'fields': ('work_experience', 'education', 'skills', 'certifications', 'projects'),
            'classes': ('collapse',)
        }),
        ('Parsing Status', {
            'fields': ('parsing_status', 'parsing_error', 'parsing_confidence')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
