"""
Serializers for job description management.
"""

from rest_framework import serializers
from .models import JobDescription, ParsedJobDescription, ResumeJobPairing


class ParsedJobDescriptionSerializer(serializers.ModelSerializer):
    """Serializer for parsed job description data."""
    
    class Meta:
        model = ParsedJobDescription
        fields = [
            'job_title', 'company_name', 'location', 'job_type', 'salary_range',
            'required_skills', 'required_experience_years', 'required_education',
            'responsibilities', 'qualifications', 'nice_to_have'
        ]


class JobDescriptionDetailSerializer(serializers.ModelSerializer):
    """Serializer for job description details."""
    parsed_data = ParsedJobDescriptionSerializer(read_only=True)
    
    class Meta:
        model = JobDescription
        fields = [
            'id', 'title', 'company', 'content', 'source_url',
            'parsing_status', 'parsing_error', 'created_at', 'updated_at', 'parsed_data'
        ]
        read_only_fields = ['id', 'parsing_status', 'parsing_error', 'created_at', 'updated_at']


class JobDescriptionListSerializer(serializers.ModelSerializer):
    """Serializer for job description list."""
    
    class Meta:
        model = JobDescription
        fields = ['id', 'title', 'company', 'parsing_status', 'created_at']


class JobDescriptionUploadSerializer(serializers.ModelSerializer):
    """Serializer for job description upload."""
    
    class Meta:
        model = JobDescription
        fields = ['title', 'company', 'content', 'source_url']


class ResumeJobPairingSerializer(serializers.ModelSerializer):
    """Serializer for resume-job pairing."""
    
    class Meta:
        model = ResumeJobPairing
        fields = ['id', 'resume', 'job_description', 'analysis_status', 'created_at']
