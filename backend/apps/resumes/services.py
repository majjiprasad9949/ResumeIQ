"""
Resume parsing and text extraction services.
"""

import re
import pdfplumber
from docx import Document
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ResumeTextExtractor:
    """Extract text from resume files (PDF, DOCX, TXT)."""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            raise
    
    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """
        Extract text from DOCX file.
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text
        """
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting DOCX: {str(e)}")
            raise
    
    @staticmethod
    def extract_from_txt(file_path: str) -> str:
        """
        Extract text from TXT file.
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Extracted text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting TXT: {str(e)}")
            raise
    
    @staticmethod
    def extract_text(file_path: str, file_format: str) -> str:
        """
        Extract text from resume file based on format.
        
        Args:
            file_path: Path to resume file
            file_format: File format (pdf, docx, txt)
            
        Returns:
            Extracted text
        """
        if file_format.lower() == 'pdf':
            return ResumeTextExtractor.extract_from_pdf(file_path)
        elif file_format.lower() == 'docx':
            return ResumeTextExtractor.extract_from_docx(file_path)
        elif file_format.lower() == 'txt':
            return ResumeTextExtractor.extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")


class ResumeParser:
    """Parse resume text and extract structured information."""
    
    # Common section headers
    SECTION_HEADERS = {
        'contact': r'(contact|personal|info|information)',
        'summary': r'(summary|objective|profile|about)',
        'experience': r'(experience|work|employment|professional)',
        'education': r'(education|academic|degree)',
        'skills': r'(skills|technical|competencies|expertise)',
        'certifications': r'(certification|certifications|license|licenses)',
        'projects': r'(projects|portfolio|work samples)',
    }
    
    # Email pattern
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Phone patterns
    PHONE_PATTERNS = [
        r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',  # US format
        r'\+\d{1,3}\s?\d{1,14}',  # International format
    ]
    
    # Date patterns
    DATE_PATTERNS = [
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}',
        r'\d{1,2}/\d{1,2}/\d{4}',
        r'\d{4}-\d{1,2}-\d{1,2}',
    ]
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict:
        """
        Extract contact information from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with contact information
        """
        contact_info = {
            'full_name': None,
            'email': None,
            'phone': None,
            'location': None,
        }
        
        # Extract email
        email_match = re.search(ResumeParser.EMAIL_PATTERN, text)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        # Extract phone
        for pattern in ResumeParser.PHONE_PATTERNS:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group(0)
                break
        
        # Extract name (usually first line or near top)
        lines = text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if line and len(line) < 100 and not any(char.isdigit() for char in line):
                # Likely a name
                contact_info['full_name'] = line
                break
        
        return contact_info
    
    @staticmethod
    def extract_section(text: str, section_name: str) -> str:
        """
        Extract a specific section from resume text.
        
        Args:
            text: Resume text
            section_name: Section name (contact, summary, experience, etc.)
            
        Returns:
            Section text
        """
        if section_name not in ResumeParser.SECTION_HEADERS:
            return ""
        
        pattern = ResumeParser.SECTION_HEADERS[section_name]
        
        # Find section header
        lines = text.split('\n')
        section_start = None
        section_end = None
        
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                section_start = i
                break
        
        if section_start is None:
            return ""
        
        # Find next section header
        for i in range(section_start + 1, len(lines)):
            if re.search(r'|'.join(ResumeParser.SECTION_HEADERS.values()), lines[i], re.IGNORECASE):
                section_end = i
                break
        
        if section_end is None:
            section_end = len(lines)
        
        section_text = '\n'.join(lines[section_start:section_end])
        return section_text.strip()
    
    @staticmethod
    def extract_skills(text: str) -> List[Dict]:
        """
        Extract skills from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of skills
        """
        skills = []
        
        # Extract skills section
        skills_section = ResumeParser.extract_section(text, 'skills')
        
        if not skills_section:
            return skills
        
        # Split by common delimiters
        skill_items = re.split(r'[,;•\n]', skills_section)
        
        for item in skill_items:
            item = item.strip()
            # Remove section header
            item = re.sub(r'(skills|technical|competencies|expertise):', '', item, flags=re.IGNORECASE)
            item = item.strip()
            
            if item and len(item) > 2 and len(item) < 100:
                skills.append({
                    'name': item,
                    'level': None,
                    'category': None,
                })
        
        return skills[:50]  # Limit to 50 skills
    
    @staticmethod
    def extract_education(text: str) -> List[Dict]:
        """
        Extract education information from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of education entries
        """
        education = []
        
        # Extract education section
        education_section = ResumeParser.extract_section(text, 'education')
        
        if not education_section:
            return education
        
        # Split by common delimiters
        entries = re.split(r'\n(?=[A-Z])', education_section)
        
        for entry in entries:
            entry = entry.strip()
            if not entry or len(entry) < 10:
                continue
            
            # Extract degree
            degree_match = re.search(r'(Bachelor|Master|PhD|Associate|Diploma|Certificate|B\.S\.|M\.S\.|B\.A\.|M\.A\.)', entry, re.IGNORECASE)
            degree = degree_match.group(0) if degree_match else None
            
            # Extract institution
            institution = None
            lines = entry.split('\n')
            if lines:
                institution = lines[0].strip()
            
            # Extract dates
            dates = re.findall(ResumeParser.DATE_PATTERNS[0], entry)
            graduation_date = dates[-1] if dates else None
            
            if degree or institution:
                education.append({
                    'degree': degree,
                    'institution': institution,
                    'graduation_date': graduation_date,
                    'gpa': None,
                    'field_of_study': None,
                })
        
        return education[:10]  # Limit to 10 entries
    
    @staticmethod
    def extract_experience(text: str) -> List[Dict]:
        """
        Extract work experience from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of experience entries
        """
        experience = []
        
        # Extract experience section
        experience_section = ResumeParser.extract_section(text, 'experience')
        
        if not experience_section:
            return experience
        
        # Split by common delimiters
        entries = re.split(r'\n(?=[A-Z])', experience_section)
        
        for entry in entries:
            entry = entry.strip()
            if not entry or len(entry) < 10:
                continue
            
            lines = entry.split('\n')
            
            # Extract job title and company
            title = None
            company = None
            
            if len(lines) >= 1:
                title = lines[0].strip()
            if len(lines) >= 2:
                company = lines[1].strip()
            
            # Extract dates
            dates = re.findall(ResumeParser.DATE_PATTERNS[0], entry)
            start_date = dates[0] if len(dates) > 0 else None
            end_date = dates[1] if len(dates) > 1 else None
            
            # Extract description
            description = '\n'.join(lines[2:]) if len(lines) > 2 else None
            
            if title or company:
                experience.append({
                    'title': title,
                    'company': company,
                    'start_date': start_date,
                    'end_date': end_date,
                    'description': description,
                })
        
        return experience[:20]  # Limit to 20 entries
    
    @staticmethod
    def extract_certifications(text: str) -> List[Dict]:
        """
        Extract certifications from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of certifications
        """
        certifications = []
        
        # Extract certifications section
        cert_section = ResumeParser.extract_section(text, 'certifications')
        
        if not cert_section:
            return certifications
        
        # Split by common delimiters
        cert_items = re.split(r'[,;•\n]', cert_section)
        
        for item in cert_items:
            item = item.strip()
            # Remove section header
            item = re.sub(r'(certification|certifications|license|licenses):', '', item, flags=re.IGNORECASE)
            item = item.strip()
            
            if item and len(item) > 2 and len(item) < 200:
                certifications.append({
                    'name': item,
                    'issuer': None,
                    'issue_date': None,
                    'expiration_date': None,
                })
        
        return certifications[:20]  # Limit to 20 certifications
    
    @staticmethod
    def extract_projects(text: str) -> List[Dict]:
        """
        Extract projects from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            List of projects
        """
        projects = []
        
        # Extract projects section
        projects_section = ResumeParser.extract_section(text, 'projects')
        
        if not projects_section:
            return projects
        
        # Split by common delimiters
        entries = re.split(r'\n(?=[A-Z])', projects_section)
        
        for entry in entries:
            entry = entry.strip()
            if not entry or len(entry) < 10:
                continue
            
            lines = entry.split('\n')
            
            # Extract project title
            title = lines[0].strip() if lines else None
            
            # Extract description
            description = '\n'.join(lines[1:]) if len(lines) > 1 else None
            
            if title:
                projects.append({
                    'title': title,
                    'description': description,
                    'technologies': None,
                })
        
        return projects[:10]  # Limit to 10 projects
    
    @staticmethod
    def extract_summary(text: str) -> Optional[str]:
        """
        Extract professional summary from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Summary text or None
        """
        summary_section = ResumeParser.extract_section(text, 'summary')
        
        if not summary_section:
            return None
        
        # Remove section header
        summary = re.sub(r'(summary|objective|profile|about):', '', summary_section, flags=re.IGNORECASE)
        summary = summary.strip()
        
        # Limit to first 500 characters
        return summary[:500] if summary else None
    
    @staticmethod
    def parse_resume(text: str) -> Dict:
        """
        Parse complete resume and extract all information.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with parsed resume data
        """
        try:
            parsed_data = {
                'full_name': None,
                'email': None,
                'phone': None,
                'location': None,
                'summary': None,
                'work_experience': [],
                'education': [],
                'skills': [],
                'certifications': [],
                'projects': [],
                'parsing_confidence': 0.0,
            }
            
            # Extract contact info
            contact_info = ResumeParser.extract_contact_info(text)
            parsed_data.update(contact_info)
            
            # Extract sections
            parsed_data['summary'] = ResumeParser.extract_summary(text)
            parsed_data['work_experience'] = ResumeParser.extract_experience(text)
            parsed_data['education'] = ResumeParser.extract_education(text)
            parsed_data['skills'] = ResumeParser.extract_skills(text)
            parsed_data['certifications'] = ResumeParser.extract_certifications(text)
            parsed_data['projects'] = ResumeParser.extract_projects(text)
            
            # Calculate confidence score
            confidence = 0.0
            if parsed_data['full_name']:
                confidence += 0.2
            if parsed_data['email']:
                confidence += 0.2
            if parsed_data['work_experience']:
                confidence += 0.2
            if parsed_data['education']:
                confidence += 0.2
            if parsed_data['skills']:
                confidence += 0.2
            
            parsed_data['parsing_confidence'] = min(confidence, 1.0)
            
            return parsed_data
        
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise
