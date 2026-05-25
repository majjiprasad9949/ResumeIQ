"""
Admin configuration for users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, PasswordResetToken, EmailVerificationToken


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin for CustomUser model."""
    list_display = ['email', 'first_name', 'last_name', 'is_email_verified', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_email_verified', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'location', 'bio', 'profile_picture')
        }),
        ('Email Verification', {
            'fields': ('is_email_verified', 'email_verified_at')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'data_processing_consent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_login_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login_at', 'email_verified_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    list_display = ['user', 'current_job_title', 'years_of_experience', 'total_resumes', 'average_ats_score']
    list_filter = ['industry', 'created_at']
    search_fields = ['user__email', 'current_job_title', 'current_company']
    readonly_fields = ['created_at', 'updated_at', 'total_resumes', 'total_optimizations', 'average_ats_score']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Current Position', {
            'fields': ('current_job_title', 'current_company', 'years_of_experience', 'industry')
        }),
        ('Target Position', {
            'fields': ('target_job_title', 'target_industry')
        }),
        ('Statistics', {
            'fields': ('total_resumes', 'total_optimizations', 'average_ats_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin for PasswordResetToken model."""
    list_display = ['user', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'used_at']
    
    fieldsets = (
        ('Token Info', {
            'fields': ('user', 'token')
        }),
        ('Status', {
            'fields': ('is_used', 'used_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at')
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """Admin for EmailVerificationToken model."""
    list_display = ['user', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'used_at']
    
    fieldsets = (
        ('Token Info', {
            'fields': ('user', 'token')
        }),
        ('Status', {
            'fields': ('is_used', 'used_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at')
        }),
    )
