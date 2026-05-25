"""
Job description models for upload and analysis.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class JobDescription(models.Model):
    """
    Job description model for storing job postings.
    """
    PARSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_descriptions')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    source_url = models.URLField(blank=True, null=True)
    
    # Parsing Status
    parsing_status = models.CharField(
        max_length=20,
        choices=PARSING_STATUS_CHOICES,
        default='pending'
    )
    parsing_error = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Job Description'
        verbose_name_plural = 'Job Descriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company}"


class ParsedJobDescription(models.Model):
    """
    Parsed job description data extracted from job posting.
    """
    job_description = models.OneToOneField(
        JobDescription,
        on_delete=models.CASCADE,
        related_name='parsed_data'
    )
    
    # Job Information
    job_title = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)  # Full-time, Part-time, etc.
    salary_range = models.CharField(max_length=255, blank=True, null=True)
    
    # Requirements
    required_skills = models.JSONField(default=list, blank=True)
    required_experience_years = models.IntegerField(blank=True, null=True)
    required_education = models.CharField(max_length=255, blank=True, null=True)
    
    # Structured Data
    responsibilities = models.JSONField(default=list, blank=True)
    qualifications = models.JSONField(default=list, blank=True)
    nice_to_have = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Parsed Job Description'
        verbose_name_plural = 'Parsed Job Descriptions'
    
    def __str__(self):
        return f"Parsed - {self.job_description.title}"


class ResumeJobPairing(models.Model):
    """
    Pairing between resume and job description for analysis.
    """
    from apps.resumes.models import Resume
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_pairings')
    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name='resume_pairings'
    )
    
    # Analysis Status
    analysis_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Resume Job Pairing'
        verbose_name_plural = 'Resume Job Pairings'
        unique_together = ['resume', 'job_description']
    
    def __str__(self):
        return f"{self.resume.title} - {self.job_description.title}"
