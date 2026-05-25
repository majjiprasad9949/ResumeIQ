"""
ATS Scoring Service for resume analysis and scoring.

This module provides the ATSScorer class which calculates ATS scores
based on multiple factors including keyword matching, skills alignment,
resume structure, experience matching, and grammar quality.

Scoring Weights:
- Keyword Match: 30%
- Skills Match: 25%
- Resume Structure: 20%
- Experience Match: 15%
- Grammar Quality: 10%
Total: 100%
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from collections import Counter

try:
    import spacy
    from spacy.language import Language
except ImportError:
    spacy = None
    Language = None

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None
    util = None

logger = logging.getLogger(__name__)


class ATSScorer:
    """
    ATS Scoring Service for calculating resume scores against job descriptions.
    
    This class provides methods to calculate various scoring components and
    combine them into a final ATS score with risk level classification.
    """
    
    # Scoring weights (must sum to 100)
    KEYWORD_MATCH_WEIGHT = 0.30
    SKILLS_MATCH_WEIGHT = 0.25
    RESUME_STRUCTURE_WEIGHT = 0.20
    EXPERIENCE_MATCH_WEIGHT = 0.15
    GRAMMAR_QUALITY_WEIGHT = 0.10
    
    # Risk level thresholds
    LOW_RISK_THRESHOLD = 75
    MODERATE_RISK_THRESHOLD = 60
    
    # Common stop words to exclude from keyword analysis
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'same', 'so', 'than', 'too', 'very',
        'just', 'also', 'if', 'because', 'while', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'about', 'own', 'should',
        'your', 'his', 'her', 'its', 'our', 'their', 'my', 'me', 'him', 'us',
        'them', 'am', 'been', 'being', 'having', 'doing', 'should', 'would',
        'could', 'ought', 'may', 'might', 'must', 'can', 'shall', 'will'
    }
    
    # Common resume section headers
    RESUME_SECTIONS = {
        'contact', 'summary', 'objective', 'professional', 'experience',
        'work', 'employment', 'education', 'skills', 'certifications',
        'projects', 'portfolio', 'languages', 'awards', 'publications',
        'volunteer', 'interests', 'references'
    }
    
    def __init__(self):
        """Initialize the ATS Scorer with NLP models."""
        self.nlp = None
        self.sentence_transformer = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize spaCy and sentence-transformer models."""
        try:
            if spacy:
                try:
                    self.nlp = spacy.load('en_core_web_sm')
                except OSError:
                    logger.warning("spaCy model 'en_core_web_sm' not found. Some features may be limited.")
        except Exception as e:
            logger.warning(f"Failed to load spaCy model: {e}")
        
        try:
            if SentenceTransformer:
                self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.warning(f"Failed to load sentence-transformer model: {e}")
    
    def calculate_ats_score(self, resume_text: str, job_description_text: str) -> Dict:
        """
        Calculate the overall ATS score for a resume against a job description.
        
        Args:
            resume_text: The full text content of the resume
            job_description_text: The full text content of the job description
        
        Returns:
            Dictionary containing:
            - overall_score: float (0-100)
            - keyword_match_score: float (0-100)
            - skills_match_score: float (0-100)
            - resume_structure_score: float (0-100)
            - experience_match_score: float (0-100)
            - grammar_quality_score: float (0-100)
            - risk_level: str ('low', 'moderate', 'high')
            - missing_keywords: list of str
            - skill_gaps: list of str
        """
        # Handle edge cases
        if not resume_text or not isinstance(resume_text, str):
            resume_text = ""
        if not job_description_text or not isinstance(job_description_text, str):
            job_description_text = ""
        
        # Calculate individual component scores
        keyword_match_score = self.calculate_keyword_match(resume_text, job_description_text)
        skills_match_score = self.calculate_skills_match(resume_text, job_description_text)
        resume_structure_score = self.calculate_resume_structure_score(resume_text)
        experience_match_score = self.calculate_experience_match(resume_text, job_description_text)
        grammar_quality_score = self.calculate_grammar_quality(resume_text)
        
        # Calculate weighted overall score
        overall_score = (
            keyword_match_score * self.KEYWORD_MATCH_WEIGHT +
            skills_match_score * self.SKILLS_MATCH_WEIGHT +
            resume_structure_score * self.RESUME_STRUCTURE_WEIGHT +
            experience_match_score * self.EXPERIENCE_MATCH_WEIGHT +
            grammar_quality_score * self.GRAMMAR_QUALITY_WEIGHT
        )
        
        # Ensure score is within valid range
        overall_score = max(0.0, min(100.0, overall_score))
        
        # Determine risk level
        risk_level = self._classify_risk_level(overall_score)
        
        # Extract missing keywords and skill gaps
        missing_keywords = self._extract_missing_keywords(resume_text, job_description_text)
        skill_gaps = self._extract_skill_gaps(resume_text, job_description_text)
        
        return {
            'overall_score': round(overall_score, 2),
            'keyword_match_score': round(keyword_match_score, 2),
            'skills_match_score': round(skills_match_score, 2),
            'resume_structure_score': round(resume_structure_score, 2),
            'experience_match_score': round(experience_match_score, 2),
            'grammar_quality_score': round(grammar_quality_score, 2),
            'risk_level': risk_level,
            'missing_keywords': missing_keywords,
            'skill_gaps': skill_gaps,
        }
    
    def calculate_keyword_match(self, resume_text: str, job_description_text: str) -> float:
        """
        Calculate keyword match score (0-100).
        
        Compares keywords from job description with those in resume.
        Uses both exact matching and semantic similarity.
        
        Args:
            resume_text: Resume text content
            job_description_text: Job description text content
        
        Returns:
            Keyword match score (0-100)
        """
        if not resume_text or not job_description_text:
            return 0.0
        
        # Extract keywords from both texts
        job_keywords = self._extract_keywords(job_description_text)
        resume_keywords = self._extract_keywords(resume_text)
        
        if not job_keywords:
            return 100.0  # No keywords to match
        
        # Count exact matches
        exact_matches = len(set(job_keywords) & set(resume_keywords))
        
        # Calculate semantic similarity for non-exact matches
        semantic_matches = 0
        if self.sentence_transformer and len(job_keywords) > exact_matches:
            semantic_matches = self._count_semantic_matches(
                [kw for kw in job_keywords if kw not in resume_keywords],
                resume_text
            )
        
        # Calculate match percentage
        total_matches = exact_matches + semantic_matches
        match_percentage = (total_matches / len(job_keywords)) * 100
        
        return min(100.0, match_percentage)
    
    def calculate_skills_match(self, resume_text: str, job_description_text: str) -> float:
        """
        Calculate skills match score (0-100).
        
        Extracts skills from both resume and job description,
        then calculates the percentage of required skills present in resume.
        
        Args:
            resume_text: Resume text content
            job_description_text: Job description text content
        
        Returns:
            Skills match score (0-100)
        """
        if not resume_text or not job_description_text:
            return 0.0
        
        # Extract skills using NLP
        resume_skills = self._extract_skills(resume_text)
        job_skills = self._extract_skills(job_description_text)
        
        if not job_skills:
            return 100.0  # No skills required
        
        # Count matched skills
        matched_skills = len(set(resume_skills) & set(job_skills))
        
        # Calculate match percentage
        match_percentage = (matched_skills / len(job_skills)) * 100
        
        return min(100.0, match_percentage)
    
    def calculate_resume_structure_score(self, resume_text: str) -> float:
        """
        Calculate resume structure score (0-100).
        
        Evaluates the presence of standard resume sections,
        formatting consistency, and ATS-friendly structure.
        
        Args:
            resume_text: Resume text content
        
        Returns:
            Resume structure score (0-100)
        """
        if not resume_text:
            return 0.0
        
        score = 0.0
        max_score = 100.0
        
        # Check for standard sections (each worth up to 20 points)
        sections_found = 0
        text_lower = resume_text.lower()
        
        for section in self.RESUME_SECTIONS:
            if section in text_lower:
                sections_found += 1
        
        # Award points for sections found (max 40 points)
        section_score = min(40.0, (sections_found / 5) * 40)
        score += section_score
        
        # Check for consistent formatting (20 points)
        formatting_score = self._evaluate_formatting_consistency(resume_text)
        score += formatting_score
        
        # Check for proper use of bullet points (20 points)
        bullet_score = self._evaluate_bullet_points(resume_text)
        score += bullet_score
        
        # Check for date consistency (20 points)
        date_score = self._evaluate_date_consistency(resume_text)
        score += date_score
        
        return min(100.0, score)
    
    def calculate_experience_match(self, resume_text: str, job_description_text: str) -> float:
        """
        Calculate experience match score (0-100).
        
        Extracts years of experience from both resume and job description,
        then calculates how well they align.
        
        Args:
            resume_text: Resume text content
            job_description_text: Job description text content
        
        Returns:
            Experience match score (0-100)
        """
        if not resume_text or not job_description_text:
            return 0.0
        
        # Extract years of experience
        resume_years = self._extract_years_of_experience(resume_text)
        required_years = self._extract_required_years(job_description_text)
        
        # If no experience info found, return neutral score
        if resume_years is None or required_years is None:
            return 50.0
        
        # Calculate match
        if required_years == 0:
            return 100.0
        
        # Score based on experience level
        if resume_years >= required_years:
            # Candidate has sufficient or more experience
            # Slight penalty for overqualification (max 5 points)
            overqualification_penalty = min(5.0, (resume_years - required_years) * 0.5)
            score = 100.0 - overqualification_penalty
        else:
            # Candidate is underqualified
            # Penalty proportional to experience gap
            experience_gap = required_years - resume_years
            score = max(0.0, 100.0 - (experience_gap * 15))
        
        return min(100.0, score)
    
    def calculate_grammar_quality(self, resume_text: str) -> float:
        """
        Calculate grammar quality score (0-100).
        
        Evaluates the quality of writing in the resume including
        sentence structure, common grammar issues, and consistency.
        
        Args:
            resume_text: Resume text content
        
        Returns:
            Grammar quality score (0-100)
        """
        if not resume_text:
            return 0.0
        
        score = 100.0
        
        # Check for common grammar issues
        issues_found = 0
        
        # Check for inconsistent tense (past vs present)
        past_tense_count = len(re.findall(r'\b(managed|developed|created|led|implemented)\b', resume_text, re.IGNORECASE))
        present_tense_count = len(re.findall(r'\b(manage|develop|create|lead|implement)\b', resume_text, re.IGNORECASE))
        
        if past_tense_count > 0 and present_tense_count > 0:
            # Mixed tense detected
            issues_found += 1
        
        # Check for weak action verbs
        weak_verbs = ['responsible for', 'worked on', 'helped', 'involved in', 'did', 'was']
        for verb in weak_verbs:
            if verb.lower() in resume_text.lower():
                issues_found += 1
        
        # Check for excessive use of personal pronouns
        pronouns = ['i ', 'me ', 'my ', 'we ', 'us ', 'our ']
        pronoun_count = sum(len(re.findall(f'\\b{p}', resume_text.lower())) for p in pronouns)
        
        if pronoun_count > 5:
            issues_found += 1
        
        # Check for spelling issues (basic check)
        # This is a simplified check - in production, use a proper spell checker
        common_misspellings = {
            'recieve': 'receive',
            'occured': 'occurred',
            'seperate': 'separate',
            'definately': 'definitely',
            'untill': 'until',
        }
        
        for misspelling in common_misspellings:
            if misspelling in resume_text.lower():
                issues_found += 1
        
        # Deduct points for each issue found
        score = max(0.0, 100.0 - (issues_found * 10))
        
        return score
    
    def _classify_risk_level(self, score: float) -> str:
        """
        Classify risk level based on ATS score.
        
        Args:
            score: ATS score (0-100)
        
        Returns:
            Risk level: 'low', 'moderate', or 'high'
        """
        if score >= self.LOW_RISK_THRESHOLD:
            return 'low'
        elif score >= self.MODERATE_RISK_THRESHOLD:
            return 'moderate'
        else:
            return 'high'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text.
        
        Args:
            text: Text to extract keywords from
        
        Returns:
            List of keywords
        """
        if not text:
            return []
        
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-z]+(?:\+\+)?\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [
            word for word in words
            if word not in self.STOP_WORDS and len(word) > 2
        ]
        
        # Remove duplicates while preserving frequency info
        return list(set(keywords))
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using NLP.
        
        Args:
            text: Text to extract skills from
        
        Returns:
            List of skills
        """
        if not text:
            return []
        
        skills = []
        
        # Common technical skills and frameworks
        technical_skills = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'git', 'jenkins', 'gitlab', 'github', 'circleci', 'travis',
            'html', 'css', 'sass', 'webpack', 'npm', 'yarn', 'gradle', 'maven',
            'rest', 'graphql', 'grpc', 'soap', 'microservices', 'api',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'agile', 'scrum', 'kanban', 'jira', 'confluence',
            'linux', 'windows', 'macos', 'unix', 'bash', 'shell',
            'excel', 'powerpoint', 'word', 'salesforce', 'sap',
            'communication', 'leadership', 'teamwork', 'problem-solving',
            'project management', 'time management', 'critical thinking',
        }
        
        text_lower = text.lower()
        
        # Find technical skills
        for skill in technical_skills:
            if skill in text_lower:
                skills.append(skill)
        
        # Use spaCy for additional skill extraction if available
        if self.nlp:
            try:
                doc = self.nlp(text[:1000000])  # Limit to first 1M chars
                for token in doc:
                    if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                        if token.text.lower() not in self.STOP_WORDS:
                            skills.append(token.text.lower())
            except Exception as e:
                logger.warning(f"Error extracting skills with spaCy: {e}")
        
        return list(set(skills))
    
    def _extract_years_of_experience(self, resume_text: str) -> Optional[int]:
        """
        Extract total years of experience from resume.
        
        Args:
            resume_text: Resume text content
        
        Returns:
            Years of experience or None if not found
        """
        if not resume_text:
            return None
        
        # Look for patterns like "5 years", "5+ years", "5-10 years"
        patterns = [
            r'(\d+)\s*\+?\s*years?\s+of\s+experience',
            r'(\d+)\s*-\s*(\d+)\s+years?\s+of\s+experience',
            r'(\d+)\s+years?\s+professional',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    # For range patterns, take the first number
                    return int(matches[0][0])
                else:
                    return int(matches[0])
        
        # If no explicit years found, try to estimate from dates
        dates = re.findall(r'(\d{4})\s*-\s*(?:present|current|now|\d{4})', resume_text, re.IGNORECASE)
        if dates:
            try:
                start_year = int(dates[0])
                current_year = 2024
                estimated_years = current_year - start_year
                return max(0, estimated_years)
            except (ValueError, IndexError):
                pass
        
        return None
    
    def _extract_required_years(self, job_description_text: str) -> Optional[int]:
        """
        Extract required years of experience from job description.
        
        Args:
            job_description_text: Job description text content
        
        Returns:
            Required years of experience or None if not found
        """
        if not job_description_text:
            return None
        
        # Look for patterns like "5 years", "5+ years", "5-10 years"
        patterns = [
            r'(\d+)\s*\+?\s*years?\s+of\s+(?:experience|expertise)',
            r'(\d+)\s*-\s*(\d+)\s+years?\s+of\s+(?:experience|expertise)',
            r'require[ds]?\s+(\d+)\s+years?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_description_text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    # For range patterns, take the first number
                    return int(matches[0][0])
                else:
                    return int(matches[0])
        
        return None
    
    def _evaluate_formatting_consistency(self, resume_text: str) -> float:
        """
        Evaluate formatting consistency in resume.
        
        Args:
            resume_text: Resume text content
        
        Returns:
            Formatting consistency score (0-20)
        """
        score = 20.0
        
        # Check for consistent spacing
        lines = resume_text.split('\n')
        if len(lines) < 5:
            score -= 5
        
        # Check for excessive special characters
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s\-\.\,\(\)\:]', resume_text))
        if special_char_count > len(resume_text) * 0.05:  # More than 5% special chars
            score -= 5
        
        return max(0.0, score)
    
    def _evaluate_bullet_points(self, resume_text: str) -> float:
        """
        Evaluate proper use of bullet points.
        
        Args:
            resume_text: Resume text content
        
        Returns:
            Bullet point score (0-20)
        """
        score = 20.0
        
        # Check for bullet points
        bullet_count = len(re.findall(r'[\•\-\*]\s+', resume_text))
        
        if bullet_count == 0:
            score -= 10
        elif bullet_count < 5:
            score -= 5
        
        return max(0.0, score)
    
    def _evaluate_date_consistency(self, resume_text: str) -> float:
        """
        Evaluate date format consistency.
        
        Args:
            resume_text: Resume text content
        
        Returns:
            Date consistency score (0-20)
        """
        score = 20.0
        
        # Find all dates
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # Month YYYY
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # DD Month YYYY
        ]
        
        date_formats_found = set()
        for pattern in date_patterns:
            if re.search(pattern, resume_text, re.IGNORECASE):
                date_formats_found.add(pattern)
        
        # Penalize if multiple date formats are used
        if len(date_formats_found) > 2:
            score -= 10
        
        return max(0.0, score)
    
    def _count_semantic_matches(self, keywords: List[str], text: str) -> int:
        """
        Count semantic matches between keywords and text.
        
        Args:
            keywords: List of keywords to match
            text: Text to search in
        
        Returns:
            Number of semantic matches
        """
        if not self.sentence_transformer or not keywords:
            return 0
        
        try:
            # Limit text to first 100k chars for performance
            text = text[:100000]
            
            # Generate embeddings
            keyword_embeddings = self.sentence_transformer.encode(keywords, convert_to_tensor=True)
            text_embedding = self.sentence_transformer.encode(text, convert_to_tensor=True)
            
            # Calculate similarity
            similarities = util.pytorch_cos_sim(keyword_embeddings, text_embedding)
            
            # Count matches with similarity > 0.7
            matches = sum(1 for sim in similarities if sim.max().item() > 0.7)
            
            return matches
        except Exception as e:
            logger.warning(f"Error in semantic matching: {e}")
            return 0
    
    def _extract_missing_keywords(self, resume_text: str, job_description_text: str) -> List[str]:
        """
        Extract keywords from job description that are missing in resume.
        
        Args:
            resume_text: Resume text content
            job_description_text: Job description text content
        
        Returns:
            List of missing keywords
        """
        job_keywords = self._extract_keywords(job_description_text)
        resume_keywords = self._extract_keywords(resume_text)
        
        # Find keywords in job description but not in resume
        missing = list(set(job_keywords) - set(resume_keywords))
        
        # Sort by frequency in job description (most frequent first)
        job_text_lower = job_description_text.lower()
        missing.sort(
            key=lambda kw: job_text_lower.count(kw),
            reverse=True
        )
        
        return missing[:10]  # Return top 10 missing keywords
    
    def _extract_skill_gaps(self, resume_text: str, job_description_text: str) -> List[str]:
        """
        Extract skills from job description that are missing in resume.
        
        Args:
            resume_text: Resume text content
            job_description_text: Job description text content
        
        Returns:
            List of skill gaps
        """
        resume_skills = self._extract_skills(resume_text)
        job_skills = self._extract_skills(job_description_text)
        
        # Find skills in job description but not in resume
        skill_gaps = list(set(job_skills) - set(resume_skills))
        
        # Sort by frequency in job description (most frequent first)
        job_text_lower = job_description_text.lower()
        skill_gaps.sort(
            key=lambda skill: job_text_lower.count(skill),
            reverse=True
        )
        
        return skill_gaps[:10]  # Return top 10 skill gaps
