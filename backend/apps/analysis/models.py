"""
Analysis models for ATS scoring and recommendations.
"""

from django.db import models
from apps.resumes.models import Resume
from apps.jobs.models import JobDescription


class ATSAnalysis(models.Model):
    """
    ATS analysis results for resume-job pairing.
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='ats_analyses')
    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name='ats_analyses'
    )
    
    # ATS Score Components
    overall_score = models.FloatField(default=0.0)  # 0-100
    keyword_match_score = models.FloatField(default=0.0)  # 0-100
    skills_match_score = models.FloatField(default=0.0)  # 0-100
    resume_structure_score = models.FloatField(default=0.0)  # 0-100
    experience_match_score = models.FloatField(default=0.0)  # 0-100
    grammar_quality_score = models.FloatField(default=0.0)  # 0-100
    
    # Risk Assessment
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
    ]
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='moderate')
    
    # Analysis Data
    missing_keywords = models.JSONField(default=list, blank=True)
    formatting_issues_data = models.JSONField(default=list, blank=True)
    skill_gaps = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'ATS Analysis'
        verbose_name_plural = 'ATS Analyses'
        unique_together = ['resume', 'job_description']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"ATS Analysis - {self.resume.title} vs {self.job_description.title}"


class Recommendation(models.Model):
    """
    Optimization recommendations for resume improvement.
    """
    RECOMMENDATION_TYPE_CHOICES = [
        ('keyword', 'Keyword Addition'),
        ('skill', 'Skill Addition'),
        ('formatting', 'Formatting'),
        ('content', 'Content Restructuring'),
        ('action_verb', 'Action Verb'),
        ('experience', 'Experience Level'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    analysis = models.ForeignKey(ATSAnalysis, on_delete=models.CASCADE, related_name='recommendations')
    
    # Recommendation Details
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    suggested_action = models.TextField()
    example = models.TextField(blank=True, null=True)
    
    # Impact
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    estimated_score_improvement = models.FloatField(default=0.0)  # 0-100
    
    # Status
    is_accepted = models.BooleanField(default=False)
    is_implemented = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
        ordering = ['-priority', '-estimated_score_improvement']
    
    def __str__(self):
        return f"{self.title} - {self.analysis.resume.title}"


class SkillGapAnalysis(models.Model):
    """
    Skill gap analysis between resume and job requirements.
    """
    SKILL_CRITICALITY_CHOICES = [
        ('must_have', 'Must Have'),
        ('nice_to_have', 'Nice to Have'),
    ]
    
    analysis = models.OneToOneField(
        ATSAnalysis,
        on_delete=models.CASCADE,
        related_name='skill_gap_analysis'
    )
    
    # Skill Data
    missing_skills = models.JSONField(default=list, blank=True)
    matched_skills = models.JSONField(default=list, blank=True)
    transferable_skills = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Skill Gap Analysis'
        verbose_name_plural = 'Skill Gap Analyses'
    
    def __str__(self):
        return f"Skill Gap - {self.analysis.resume.title}"


class FormattingIssue(models.Model):
    """
    Formatting issues detected in resume.
    """
    ISSUE_SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]
    
    analysis = models.ForeignKey(
        ATSAnalysis,
        on_delete=models.CASCADE,
        related_name='formatting_issues'
    )
    
    # Issue Details
    issue_type = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=ISSUE_SEVERITY_CHOICES)
    suggested_fix = models.TextField()
    impact_on_parsing = models.CharField(max_length=255, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Formatting Issue'
        verbose_name_plural = 'Formatting Issues'
    
    def __str__(self):
        return f"{self.issue_type} - {self.analysis.resume.title}"
