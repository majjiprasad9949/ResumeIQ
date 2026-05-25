"""
Admin configuration for AI app.
"""

from django.contrib import admin
from .models import KeywordExtraction, SemanticSimilarity, NLPModel


@admin.register(KeywordExtraction)
class KeywordExtractionAdmin(admin.ModelAdmin):
    """Admin for KeywordExtraction model."""
    list_display = ['source_type', 'created_at']
    list_filter = ['source_type', 'created_at']
    search_fields = ['content_hash']
    readonly_fields = ['created_at']


@admin.register(SemanticSimilarity)
class SemanticSimilarityAdmin(admin.ModelAdmin):
    """Admin for SemanticSimilarity model."""
    list_display = ['resume_id', 'job_id', 'overall_similarity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['resume_id', 'job_id']
    readonly_fields = ['created_at']


@admin.register(NLPModel)
class NLPModelAdmin(admin.ModelAdmin):
    """Admin for NLPModel model."""
    list_display = ['model_name', 'model_type', 'version', 'is_active', 'last_used_at']
    list_filter = ['model_type', 'is_active', 'loaded_at']
    search_fields = ['model_name']
    readonly_fields = ['loaded_at']
