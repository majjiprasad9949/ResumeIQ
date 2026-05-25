"""
Resume models for upload, storage, and versioning.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils import timezone

User = get_user_model()


class Resume(models.Model):
    """
    Resume model for storing user resumes.
    """
    RESUME_FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('txt', 'TXT'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='resumes/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])]
    )
    file_format = models.CharField(max_length=10, choices=RESUME_FORMAT_CHOICES)
    file_size = models.IntegerField()  # in bytes
    
    # Raw text extracted from file
    raw_text = models.TextField(blank=True, null=True)
    
    # Metadata
    is_current = models.BooleanField(default=True)
    version_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_current']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def get_file_extension(self):
        """Get file extension from filename."""
        return self.file.name.split('.')[-1].lower()


class ResumeVersion(models.Model):
    """
    Resume version tracking for optimization history.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    file = models.FileField(upload_to='resume_versions/%Y/%m/%d/')
    raw_text = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Resume Version'
        verbose_name_plural = 'Resume Versions'
        ordering = ['-version_number']
        unique_together = ['resume', 'version_number']
        indexes = [
            models.Index(fields=['resume', '-version_number']),
        ]
    
    def __str__(self):
        return f"{self.resume.title} - v{self.version_number}"


class ParsedResume(models.Model):
    """
    Parsed resume data extracted from uploaded resume.
    """
    PARSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='parsed_data')
    
    # Contact Information
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    # Professional Summary
    summary = models.TextField(blank=True, null=True)
    
    # Structured Data (JSON)
    # Each item: {title, company, start_date, end_date, description}
    work_experience = models.JSONField(default=list, blank=True)
    
    # Each item: {degree, institution, graduation_date, gpa, field_of_study}
    education = models.JSONField(default=list, blank=True)
    
    # Each item: {name, level, category}
    skills = models.JSONField(default=list, blank=True)
    
    # Each item: {name, issuer, issue_date, expiration_date}
    certifications = models.JSONField(default=list, blank=True)
    
    # Each item: {title, description, technologies}
    projects = models.JSONField(default=list, blank=True)
    
    # Parsing Status
    parsing_status = models.CharField(
        max_length=20,
        choices=PARSING_STATUS_CHOICES,
        default='pending'
    )
    parsing_error = models.TextField(blank=True, null=True)
    parsing_confidence = models.FloatField(default=0.0)  # 0-1 confidence score
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Parsed Resume'
        verbose_name_plural = 'Parsed Resumes'
        indexes = [
            models.Index(fields=['parsing_status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Parsed - {self.resume.title}"
    
    def mark_as_processing(self):
        """Mark parsing as in progress."""
        self.parsing_status = 'processing'
        self.save(update_fields=['parsing_status'])
    
    def mark_as_completed(self):
        """Mark parsing as completed."""
        self.parsing_status = 'completed'
        self.updated_at = timezone.now()
        self.save(update_fields=['parsing_status', 'updated_at'])
    
    def mark_as_failed(self, error_message):
        """Mark parsing as failed."""
        self.parsing_status = 'failed'
        self.parsing_error = error_message
        self.updated_at = timezone.now()
        self.save(update_fields=['parsing_status', 'parsing_error', 'updated_at'])
