"""
AI models for NLP processing and analysis.
"""

from django.db import models


class KeywordExtraction(models.Model):
    """
    Keyword extraction results from resume or job description.
    """
    KEYWORD_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('soft_skill', 'Soft Skill'),
        ('industry', 'Industry-Specific'),
    ]
    
    # Reference to source document
    content_hash = models.CharField(max_length=255, unique=True)
    source_type = models.CharField(max_length=50)  # 'resume' or 'job_description'
    
    # Extracted Keywords
    keywords = models.JSONField(default=list)  # List of {keyword, type, frequency, score}
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Keyword Extraction'
        verbose_name_plural = 'Keyword Extractions'
    
    def __str__(self):
        return f"Keywords - {self.source_type}"


class SemanticSimilarity(models.Model):
    """
    Semantic similarity scores between resume and job content.
    """
    # References
    resume_id = models.IntegerField()
    job_id = models.IntegerField()
    
    # Similarity Scores
    overall_similarity = models.FloatField()  # 0-1
    experience_similarity = models.FloatField()  # 0-1
    skills_similarity = models.FloatField()  # 0-1
    
    # Detailed Results
    similar_experiences = models.JSONField(default=list)
    similar_skills = models.JSONField(default=list)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Semantic Similarity'
        verbose_name_plural = 'Semantic Similarities'
        unique_together = ['resume_id', 'job_id']
    
    def __str__(self):
        return f"Similarity - Resume {self.resume_id} vs Job {self.job_id}"


class NLPModel(models.Model):
    """
    Tracking of NLP models used for analysis.
    """
    MODEL_TYPE_CHOICES = [
        ('spacy', 'spaCy'),
        ('sentence_transformer', 'Sentence Transformer'),
        ('sklearn', 'scikit-learn'),
    ]
    
    model_name = models.CharField(max_length=255, unique=True)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    version = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    loaded_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'NLP Model'
        verbose_name_plural = 'NLP Models'
    
    def __str__(self):
        return f"{self.model_name} ({self.model_type})"
