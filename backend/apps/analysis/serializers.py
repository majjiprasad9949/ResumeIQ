"""
Serializers for analysis results.
"""

from rest_framework import serializers
from .models import ATSAnalysis, Recommendation, SkillGapAnalysis, FormattingIssue


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for recommendations."""
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'recommendation_type', 'title', 'description', 'suggested_action',
            'example', 'priority', 'estimated_score_improvement', 'is_accepted', 'is_implemented'
        ]


class SkillGapAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for skill gap analysis."""
    
    class Meta:
        model = SkillGapAnalysis
        fields = ['missing_skills', 'matched_skills', 'transferable_skills']


class FormattingIssueSerializer(serializers.ModelSerializer):
    """Serializer for formatting issues."""
    
    class Meta:
        model = FormattingIssue
        fields = ['issue_type', 'description', 'severity', 'suggested_fix', 'impact_on_parsing']


class ATSAnalysisDetailSerializer(serializers.ModelSerializer):
    """Serializer for ATS analysis details."""
    recommendations = RecommendationSerializer(many=True, read_only=True)
    skill_gap_analysis = SkillGapAnalysisSerializer(read_only=True)
    formatting_issues = FormattingIssueSerializer(many=True, read_only=True)
    
    class Meta:
        model = ATSAnalysis
        fields = [
            'id', 'resume', 'job_description', 'overall_score', 'keyword_match_score',
            'skills_match_score', 'resume_structure_score', 'experience_match_score',
            'grammar_quality_score', 'risk_level', 'missing_keywords', 'skill_gaps',
            'created_at', 'updated_at', 'recommendations', 'skill_gap_analysis',
            'formatting_issues'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ATSAnalysisListSerializer(serializers.ModelSerializer):
    """Serializer for ATS analysis list."""
    
    class Meta:
        model = ATSAnalysis
        fields = ['id', 'resume', 'job_description', 'overall_score', 'risk_level', 'created_at']
