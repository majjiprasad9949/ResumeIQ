"""
Admin configuration for analysis app.
"""

from django.contrib import admin
from .models import ATSAnalysis, Recommendation, SkillGapAnalysis, FormattingIssue


@admin.register(ATSAnalysis)
class ATSAnalysisAdmin(admin.ModelAdmin):
    """Admin for ATSAnalysis model."""
    list_display = ['resume', 'job_description', 'overall_score', 'risk_level', 'created_at']
    list_filter = ['risk_level', 'created_at']
    search_fields = ['resume__title', 'job_description__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Admin for Recommendation model."""
    list_display = ['title', 'analysis', 'recommendation_type', 'priority', 'is_implemented']
    list_filter = ['recommendation_type', 'priority', 'is_implemented', 'created_at']
    search_fields = ['title', 'analysis__resume__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SkillGapAnalysis)
class SkillGapAnalysisAdmin(admin.ModelAdmin):
    """Admin for SkillGapAnalysis model."""
    list_display = ['analysis', 'created_at']
    list_filter = ['created_at']
    search_fields = ['analysis__resume__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FormattingIssue)
class FormattingIssueAdmin(admin.ModelAdmin):
    """Admin for FormattingIssue model."""
    list_display = ['issue_type', 'analysis', 'severity', 'created_at']
    list_filter = ['severity', 'created_at']
    search_fields = ['issue_type', 'analysis__resume__title']
    readonly_fields = ['created_at']
