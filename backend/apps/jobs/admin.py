"""
Admin configuration for jobs app.
"""

from django.contrib import admin
from .models import JobDescription, ParsedJobDescription, ResumeJobPairing


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    """Admin for JobDescription model."""
    list_display = ['title', 'company', 'user', 'parsing_status', 'created_at']
    list_filter = ['parsing_status', 'created_at']
    search_fields = ['title', 'company', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ParsedJobDescription)
class ParsedJobDescriptionAdmin(admin.ModelAdmin):
    """Admin for ParsedJobDescription model."""
    list_display = ['job_description', 'job_title', 'company_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['job_title', 'company_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ResumeJobPairing)
class ResumeJobPairingAdmin(admin.ModelAdmin):
    """Admin for ResumeJobPairing model."""
    list_display = ['resume', 'job_description', 'analysis_status', 'created_at']
    list_filter = ['analysis_status', 'created_at']
    search_fields = ['resume__title', 'job_description__title']
    readonly_fields = ['created_at', 'updated_at']
