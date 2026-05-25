"""
Serializers for resume management.
"""

from rest_framework import serializers
from django.core.files.storage import default_storage
from .models import Resume, ResumeVersion, ParsedResume


class ParsedResumeSerializer(serializers.ModelSerializer):
    """Serializer for parsed resume data."""
    
    class Meta:
        model = ParsedResume
        fields = [
            'full_name', 'email', 'phone', 'location', 'summary',
            'work_experience', 'education', 'skills', 'certifications',
            'projects', 'parsing_status', 'parsing_error', 'parsing_confidence',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'parsing_status', 'parsing_error', 'parsing_confidence',
            'created_at', 'updated_at'
        ]


class ResumeVersionSerializer(serializers.ModelSerializer):
    """Serializer for resume versions."""
    
    class Meta:
        model = ResumeVersion
        fields = ['id', 'version_number', 'created_at']
        read_only_fields = ['id', 'version_number', 'created_at']


class ResumeDetailSerializer(serializers.ModelSerializer):
    """Serializer for resume details with parsed data."""
    parsed_data = ParsedResumeSerializer(read_only=True)
    versions = ResumeVersionSerializer(read_only=True, many=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = [
            'id', 'title', 'file', 'file_url', 'file_format', 'file_size',
            'is_current', 'version_number', 'raw_text',
            'created_at', 'updated_at', 'parsed_data', 'versions'
        ]
        read_only_fields = [
            'id', 'file_size', 'version_number', 'raw_text',
            'created_at', 'updated_at', 'parsed_data', 'versions'
        ]
    
    def get_file_url(self, obj):
        """Get absolute URL for file."""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ResumeListSerializer(serializers.ModelSerializer):

    parsed_data = ParsedResumeSerializer(
        read_only=True
    )

    file_url = serializers.SerializerMethodField()

    class Meta:

        model = Resume

        fields = [

            'id',
            'title',
            'file',
            'file_url',
            'file_format',
            'file_size',
            'is_current',
            'version_number',
            'created_at',
            'parsed_data'

        ]


    def get_file_url(

        self,
        obj

    ):

        request = self.context.get(
            'request'
        )

        if obj.file:

            return request.build_absolute_uri(

                obj.file.url

            )

        return None


class ResumeUploadSerializer(serializers.ModelSerializer):
    """Serializer for resume upload."""
    
    class Meta:
        model = Resume
        fields = ['title', 'file']
    
    def validate_file(self, value):
        """Validate file size and format."""
        # Check file size (10MB max)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must not exceed 10MB.")
        
        # Check file extension
        allowed_extensions = ['pdf', 'docx', 'txt']
        file_extension = value.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"File format not supported. Allowed formats: {', '.join(allowed_extensions)}"
            )
        
        return value
    
    def validate_title(self, value):
        """Validate resume title."""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Resume title cannot be empty.")
        
        if len(value) > 255:
            raise serializers.ValidationError("Resume title must not exceed 255 characters.")
        
        return value


class ResumeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating resume information."""
    
    class Meta:
        model = Resume
        fields = ['title', 'is_current']


class ResumeComparisonSerializer(serializers.Serializer):
    """Serializer for comparing two resume versions."""
    resume_id_1 = serializers.UUIDField()
    resume_id_2 = serializers.UUIDField()
    
    def validate(self, data):
        """Validate that both resumes exist and belong to same user."""
        if data['resume_id_1'] == data['resume_id_2']:
            raise serializers.ValidationError("Cannot compare resume with itself.")
        return data

