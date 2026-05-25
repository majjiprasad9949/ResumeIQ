"""
Tests for ATS Scoring Service.
"""

import pytest
from .services import ATSScorer


class TestATSScorer:
    """Test cases for ATSScorer class."""
    
    @pytest.fixture
    def scorer(self):
        """Create an ATSScorer instance."""
        return ATSScorer()
    
    @pytest.fixture
    def sample_resume(self):
        """Sample resume text."""
        return """
        John Doe
        john@example.com | (555) 123-4567 | New York, NY
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 5 years of experience in Python and JavaScript.
        
        WORK EXPERIENCE
        Senior Software Engineer | Tech Corp | 2020 - Present
        - Developed REST APIs using Django and FastAPI
        - Implemented microservices architecture with Docker and Kubernetes
        - Led team of 3 engineers on cloud migration project
        - Improved application performance by 40% through optimization
        
        Software Engineer | StartUp Inc | 2018 - 2020
        - Built React frontend applications
        - Implemented CI/CD pipelines with Jenkins
        - Managed PostgreSQL databases
        
        EDUCATION
        Bachelor of Science in Computer Science | State University | 2018
        
        SKILLS
        Languages: Python, JavaScript, TypeScript, SQL
        Frameworks: Django, FastAPI, React, Angular
        Tools: Docker, Kubernetes, AWS, Git, Jenkins
        Databases: PostgreSQL, MongoDB, Redis
        """
    
    @pytest.fixture
    def sample_job_description(self):
        """Sample job description text."""
        return """
        Senior Software Engineer
        Tech Corp
        
        We are looking for a Senior Software Engineer with 5+ years of experience.
        
        RESPONSIBILITIES
        - Design and develop scalable REST APIs
        - Implement microservices architecture
        - Lead technical discussions and code reviews
        - Mentor junior engineers
        
        REQUIRED SKILLS
        - Python (5+ years)
        - JavaScript/TypeScript
        - Docker and Kubernetes
        - AWS or similar cloud platform
        - PostgreSQL or similar relational database
        - REST API design
        - Microservices architecture
        
        NICE TO HAVE
        - React or Angular experience
        - CI/CD pipeline experience
        - MongoDB experience
        - Leadership experience
        
        EDUCATION
        Bachelor's degree in Computer Science or related field
        """
    
    def test_calculate_ats_score_returns_valid_structure(self, scorer, sample_resume, sample_job_description):
        """Test that calculate_ats_score returns the correct structure."""
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        
        # Check all required fields are present
        assert 'overall_score' in result
        assert 'keyword_match_score' in result
        assert 'skills_match_score' in result
        assert 'resume_structure_score' in result
        assert 'experience_match_score' in result
        assert 'grammar_quality_score' in result
        assert 'risk_level' in result
        assert 'missing_keywords' in result
        assert 'skill_gaps' in result
    
    def test_ats_score_range_validity(self, scorer, sample_resume, sample_job_description):
        """Test that ATS score is always between 0 and 100."""
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        
        assert 0 <= result['overall_score'] <= 100
        assert 0 <= result['keyword_match_score'] <= 100
        assert 0 <= result['skills_match_score'] <= 100
        assert 0 <= result['resume_structure_score'] <= 100
        assert 0 <= result['experience_match_score'] <= 100
        assert 0 <= result['grammar_quality_score'] <= 100
    
    def test_ats_score_component_weights_sum_to_100(self, scorer, sample_resume, sample_job_description):
        """Test that weighted components sum to overall score."""
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        
        # Calculate weighted sum
        weighted_sum = (
            result['keyword_match_score'] * scorer.KEYWORD_MATCH_WEIGHT +
            result['skills_match_score'] * scorer.SKILLS_MATCH_WEIGHT +
            result['resume_structure_score'] * scorer.RESUME_STRUCTURE_WEIGHT +
            result['experience_match_score'] * scorer.EXPERIENCE_MATCH_WEIGHT +
            result['grammar_quality_score'] * scorer.GRAMMAR_QUALITY_WEIGHT
        )
        
        # Allow small floating point difference
        assert abs(weighted_sum - result['overall_score']) < 0.1
    
    def test_risk_level_classification_low(self, scorer):
        """Test risk level classification for low risk (>= 75)."""
        result = scorer.calculate_ats_score(
            "Python Django REST API microservices Docker Kubernetes AWS PostgreSQL",
            "Python Django REST API microservices Docker Kubernetes AWS PostgreSQL"
        )
        
        if result['overall_score'] >= 75:
            assert result['risk_level'] == 'low'
    
    def test_risk_level_classification_moderate(self, scorer):
        """Test risk level classification for moderate risk (60-74)."""
        # Create a scenario that should result in moderate risk
        resume = "Some Python experience"
        job = "Need 5 years Python, Docker, Kubernetes, AWS, PostgreSQL, React, Angular"
        
        result = scorer.calculate_ats_score(resume, job)
        
        if 60 <= result['overall_score'] < 75:
            assert result['risk_level'] == 'moderate'
    
    def test_risk_level_classification_high(self, scorer):
        """Test risk level classification for high risk (< 60)."""
        result = scorer.calculate_ats_score(
            "Basic resume",
            "Need 10 years Python, Docker, Kubernetes, AWS, PostgreSQL, React, Angular, Rust, Go"
        )
        
        if result['overall_score'] < 60:
            assert result['risk_level'] == 'high'
    
    def test_keyword_match_score_range(self, scorer, sample_resume, sample_job_description):
        """Test that keyword match score is between 0 and 100."""
        score = scorer.calculate_keyword_match(sample_resume, sample_job_description)
        assert 0 <= score <= 100
    
    def test_keyword_match_with_empty_resume(self, scorer, sample_job_description):
        """Test keyword match with empty resume."""
        score = scorer.calculate_keyword_match("", sample_job_description)
        assert score == 0.0
    
    def test_keyword_match_with_empty_job_description(self, scorer, sample_resume):
        """Test keyword match with empty job description."""
        score = scorer.calculate_keyword_match(sample_resume, "")
        assert score == 0.0
    
    def test_skills_match_score_range(self, scorer, sample_resume, sample_job_description):
        """Test that skills match score is between 0 and 100."""
        score = scorer.calculate_skills_match(sample_resume, sample_job_description)
        assert 0 <= score <= 100
    
    def test_resume_structure_score_range(self, scorer, sample_resume):
        """Test that resume structure score is between 0 and 100."""
        score = scorer.calculate_resume_structure_score(sample_resume)
        assert 0 <= score <= 100
    
    def test_resume_structure_with_empty_resume(self, scorer):
        """Test resume structure score with empty resume."""
        score = scorer.calculate_resume_structure_score("")
        assert score == 0.0
    
    def test_experience_match_score_range(self, scorer, sample_resume, sample_job_description):
        """Test that experience match score is between 0 and 100."""
        score = scorer.calculate_experience_match(sample_resume, sample_job_description)
        assert 0 <= score <= 100
    
    def test_grammar_quality_score_range(self, scorer, sample_resume):
        """Test that grammar quality score is between 0 and 100."""
        score = scorer.calculate_grammar_quality(sample_resume)
        assert 0 <= score <= 100
    
    def test_grammar_quality_with_empty_resume(self, scorer):
        """Test grammar quality score with empty resume."""
        score = scorer.calculate_grammar_quality("")
        assert score == 0.0
    
    def test_missing_keywords_is_list(self, scorer, sample_resume, sample_job_description):
        """Test that missing keywords is a list."""
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        assert isinstance(result['missing_keywords'], list)
    
    def test_skill_gaps_is_list(self, scorer, sample_resume, sample_job_description):
        """Test that skill gaps is a list."""
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        assert isinstance(result['skill_gaps'], list)
    
    def test_missing_keywords_subset_property(self, scorer, sample_resume, sample_job_description):
        """Test that missing keywords are subset of job keywords."""
        result = scorer.calculate_ats_score(sample_resume, sample_job_description)
        job_keywords = scorer._extract_keywords(sample_job_description)
        
        # All missing keywords should be in job keywords
        for keyword in result['missing_keywords']:
            assert keyword in job_keywords or keyword.lower() in sample_job_description.lower()
    
    def test_extract_keywords_returns_list(self, scorer):
        """Test that extract_keywords returns a list."""
        keywords = scorer._extract_keywords("Python Django REST API")
        assert isinstance(keywords, list)
    
    def test_extract_keywords_filters_stop_words(self, scorer):
        """Test that extract_keywords filters stop words."""
        keywords = scorer._extract_keywords("the and or but in on at to for")
        # Should be empty or very small since all are stop words
        assert len(keywords) == 0
    
    def test_extract_skills_returns_list(self, scorer):
        """Test that extract_skills returns a list."""
        skills = scorer._extract_skills("Python Django React Docker")
        assert isinstance(skills, list)
    
    def test_extract_years_of_experience_with_explicit_years(self, scorer):
        """Test extracting explicit years of experience."""
        text = "I have 5 years of experience in software development"
        years = scorer._extract_years_of_experience(text)
        assert years == 5
    
    def test_extract_years_of_experience_with_range(self, scorer):
        """Test extracting years from range."""
        text = "5-10 years of experience required"
        years = scorer._extract_years_of_experience(text)
        # Should extract the first number in the range
        assert years in [5, 10]  # Either is acceptable
    
    def test_extract_required_years_from_job_description(self, scorer):
        """Test extracting required years from job description."""
        text = "We require 5+ years of experience"
        years = scorer._extract_required_years(text)
        assert years == 5
    
    def test_classify_risk_level_low(self, scorer):
        """Test risk level classification for low risk."""
        risk = scorer._classify_risk_level(80)
        assert risk == 'low'
    
    def test_classify_risk_level_moderate(self, scorer):
        """Test risk level classification for moderate risk."""
        risk = scorer._classify_risk_level(70)
        assert risk == 'moderate'
    
    def test_classify_risk_level_high(self, scorer):
        """Test risk level classification for high risk."""
        risk = scorer._classify_risk_level(50)
        assert risk == 'high'
    
    def test_ats_score_with_none_values(self, scorer):
        """Test that ATS score handles None values gracefully."""
        result = scorer.calculate_ats_score(None, None)
        assert result['overall_score'] == 0.0
    
    def test_ats_score_consistency(self, scorer, sample_resume, sample_job_description):
        """Test that ATS score is consistent across multiple calls."""
        result1 = scorer.calculate_ats_score(sample_resume, sample_job_description)
        result2 = scorer.calculate_ats_score(sample_resume, sample_job_description)
        
        assert result1['overall_score'] == result2['overall_score']
        assert result1['risk_level'] == result2['risk_level']


class TestATSScorerEdgeCases:
    """Test edge cases for ATSScorer."""
    
    @pytest.fixture
    def scorer(self):
        """Create an ATSScorer instance."""
        return ATSScorer()
    
    def test_very_long_resume(self, scorer):
        """Test with very long resume text."""
        long_resume = "Python " * 10000
        job_desc = "Python Django"
        
        result = scorer.calculate_ats_score(long_resume, job_desc)
        assert 0 <= result['overall_score'] <= 100
    
    def test_special_characters_in_text(self, scorer):
        """Test with special characters."""
        resume = "C++ C# .NET @#$%^&*()"
        job_desc = "C++ C# .NET"
        
        result = scorer.calculate_ats_score(resume, job_desc)
        assert 0 <= result['overall_score'] <= 100
    
    def test_unicode_characters(self, scorer):
        """Test with unicode characters."""
        resume = "Développeur Python 中文 العربية"
        job_desc = "Python Developer"
        
        result = scorer.calculate_ats_score(resume, job_desc)
        assert 0 <= result['overall_score'] <= 100
    
    def test_numbers_in_text(self, scorer):
        """Test with numbers."""
        resume = "5 years 2020-2024 $100k"
        job_desc = "5+ years 2024"
        
        result = scorer.calculate_ats_score(resume, job_desc)
        assert 0 <= result['overall_score'] <= 100
    
    def test_mixed_case_keywords(self, scorer):
        """Test with mixed case keywords."""
        resume = "PYTHON python Python PyThOn"
        job_desc = "python"
        
        result = scorer.calculate_ats_score(resume, job_desc)
        assert result['keyword_match_score'] > 0
