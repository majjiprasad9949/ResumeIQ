# ResumeIQ + ATS Simulator - Design Document

## Overview

The ResumeIQ + ATS Simulator is a full-stack web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS) and receive AI-powered recommendations. The system combines a React.js frontend, Django REST Framework backend, PostgreSQL database, and machine learning models to deliver intelligent resume analysis and optimization.

### Key Design Principles

1. **Modularity**: Separate concerns into distinct services (parsing, analysis, scoring, recommendations)
2. **Scalability**: Asynchronous processing for long-running tasks (parsing, analysis)
3. **Security**: JWT-based authentication, encrypted data at rest, HTTPS for all communications
4. **Extensibility**: Plugin architecture for NLP models and analysis engines
5. **Performance**: Caching for frequently accessed data, optimized database queries

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React.js)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Auth Module  │  │ Resume Mgmt  │  │ Analysis UI  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway (Django REST)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Auth API     │  │ Resume API   │  │ Analysis API │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Auth Service │  │ Resume Svc   │  │ Analysis Svc │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    NLP/ML Pipeline                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Parser       │  │ Keyword Ext  │  │ Semantic Ana │           │
│  │ (spaCy)      │  │ (spaCy)      │  │ (transformers)           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ PostgreSQL   │  │ Redis Cache  │  │ S3 Storage   │           │
│  │ (Primary DB) │  │ (Sessions)   │  │ (Files)      │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Layered Architecture

**Presentation Layer (Frontend)**
- React.js components for user interface
- Redux for state management
- Axios for API communication
- Real-time validation and feedback

**API Layer (Django REST Framework)**
- RESTful endpoints for all operations
- JWT authentication middleware
- Request/response serialization
- Error handling and logging

**Business Logic Layer**
- Service classes for core functionality
- Orchestration of NLP/ML operations
- Business rule enforcement
- Transaction management

**NLP/ML Pipeline Layer**
- Resume parsing (spaCy, PyPDF2, python-docx)
- Keyword extraction (spaCy NER, TF-IDF)
- Semantic analysis (sentence-transformers)
- ATS scoring algorithm

**Data Layer**
- PostgreSQL for persistent data
- Redis for caching and sessions
- AWS S3 for file storage
- Elasticsearch for full-text search (optional)

## Components and Interfaces

### Core Components

#### 1. Authentication Service
**Responsibility**: User registration, login, token management, password reset

**Key Methods**:
- `register(email, password, full_name)` → JWT token
- `login(email, password)` → JWT token
- `refresh_token(token)` → New JWT token
- `validate_token(token)` → User ID or None
- `reset_password(email)` → Reset token
- `verify_reset_token(token, new_password)` → Success/Failure

**Dependencies**: PostgreSQL, Email Service, JWT Library

#### 2. Resume Upload Manager
**Responsibility**: File upload, validation, storage, text extraction

**Key Methods**:
- `upload_resume(file, user_id)` → Resume ID
- `validate_file(file)` → Validation result
- `extract_text(file_path)` → Text content
- `store_file(file, resume_id)` → Storage path
- `delete_resume(resume_id)` → Success/Failure

**Dependencies**: S3, File validation libraries, Text extraction libraries

#### 3. Resume Parser
**Responsibility**: Extract structured data from resume text

**Key Methods**:
- `parse_resume(text)` → Structured resume data
- `extract_contact_info(text)` → Contact information
- `extract_experience(text)` → Work experience entries
- `extract_education(text)` → Education entries
- `extract_skills(text)` → Skills list
- `normalize_dates(date_string)` → Normalized date

**Dependencies**: spaCy, regex patterns, date parsing libraries

**Output Structure**:
```python
{
  "contact": {
    "name": str,
    "email": str,
    "phone": str,
    "location": str
  },
  "summary": str,
  "experience": [
    {
      "job_title": str,
      "company": str,
      "start_date": date,
      "end_date": date,
      "description": str
    }
  ],
  "education": [
    {
      "degree": str,
      "institution": str,
      "graduation_date": date,
      "gpa": float
    }
  ],
  "skills": [str],
  "certifications": [str]
}
```

#### 4. Job Description Parser
**Responsibility**: Extract requirements and keywords from job descriptions

**Key Methods**:
- `parse_job_description(text)` → Structured job data
- `extract_requirements(text)` → Requirements list
- `extract_skills(text)` → Required skills
- `extract_experience_level(text)` → Experience level
- `identify_keywords(text)` → Important keywords

**Output Structure**:
```python
{
  "title": str,
  "company": str,
  "requirements": [str],
  "responsibilities": [str],
  "required_skills": [str],
  "nice_to_have_skills": [str],
  "experience_level": str,  # junior, mid, senior
  "years_required": int,
  "keywords": [str]
}
```

#### 5. Keyword Extractor
**Responsibility**: Identify and rank important keywords using NLP

**Key Methods**:
- `extract_keywords(text, keyword_type)` → Keywords with scores
- `extract_technical_keywords(text)` → Technical keywords
- `extract_soft_skills(text)` → Soft skills
- `extract_industry_terms(text)` → Industry-specific terms
- `rank_keywords(keywords, job_description)` → Ranked keywords

**Dependencies**: spaCy, scikit-learn (TF-IDF), custom keyword databases

#### 6. Semantic Analyzer
**Responsibility**: Calculate semantic similarity between resume and job description

**Key Methods**:
- `calculate_similarity(text1, text2)` → Similarity score (0-1)
- `analyze_experience_relevance(experience, job_desc)` → Relevance scores
- `analyze_skills_relevance(skills, job_desc)` → Relevance scores
- `identify_transferable_skills(resume, job_desc)` → Transferable skills

**Dependencies**: sentence-transformers, pre-trained embeddings

#### 7. ATS Scorer
**Responsibility**: Calculate ATS score based on multiple factors

**Key Methods**:
- `calculate_ats_score(resume, job_description)` → Score (0-100)
- `calculate_keyword_match(resume, job_desc)` → Keyword match %
- `calculate_formatting_score(resume)` → Formatting score
- `calculate_skill_alignment(resume, job_desc)` → Skill alignment %
- `calculate_experience_match(resume, job_desc)` → Experience match %
- `get_score_breakdown(resume, job_desc)` → Component scores

**Scoring Algorithm**:
```
ATS_Score = (
  keyword_match * 0.40 +
  formatting_score * 0.20 +
  skill_alignment * 0.25 +
  experience_match * 0.15
) * 100
```

#### 8. Formatting Validator
**Responsibility**: Check resume formatting for ATS compatibility

**Key Methods**:
- `validate_formatting(resume_text)` → Formatting issues
- `check_section_headers(text)` → Header validation
- `check_date_consistency(text)` → Date format consistency
- `check_special_characters(text)` → Special character analysis
- `check_column_layout(text)` → Column layout detection
- `estimate_parsing_impact(issues)` → Impact score

#### 9. Recommendation Engine
**Responsibility**: Generate optimization suggestions

**Key Methods**:
- `generate_recommendations(resume, job_desc, ats_score)` → Recommendations list
- `suggest_keywords(missing_keywords)` → Keyword suggestions
- `suggest_restructuring(experience, job_desc)` → Restructuring suggestions
- `suggest_skills(skill_gaps)` → Skill suggestions
- `suggest_formatting(formatting_issues)` → Formatting suggestions
- `prioritize_recommendations(recommendations)` → Prioritized list
- `estimate_score_improvement(recommendation)` → Estimated improvement

**Recommendation Structure**:
```python
{
  "id": str,
  "category": str,  # keyword, skill, formatting, experience
  "priority": int,  # 1-5
  "title": str,
  "description": str,
  "action": str,
  "example": str,
  "estimated_improvement": float  # 0-100
}
```

#### 10. Resume Version Manager
**Responsibility**: Track resume versions and changes

**Key Methods**:
- `create_version(resume_id, content)` → Version ID
- `get_version_history(resume_id)` → Version list
- `compare_versions(version_id1, version_id2)` → Differences
- `revert_to_version(resume_id, version_id)` → Success/Failure
- `recalculate_scores(resume_id)` → Updated scores

#### 11. Skill Gap Analyzer
**Responsibility**: Identify missing skills and learning opportunities

**Key Methods**:
- `analyze_skill_gaps(resume, job_desc)` → Skill gaps
- `categorize_skills(skills)` → Categorized skills
- `identify_transferable_skills(resume, job_desc)` → Transferable skills
- `suggest_learning_resources(skill)` → Learning resources

#### 12. Experience Matcher
**Responsibility**: Match experience levels between resume and job

**Key Methods**:
- `extract_total_experience(resume)` → Years of experience
- `extract_relevant_experience(resume, job_desc)` → Relevant years
- `extract_required_experience(job_desc)` → Required years
- `match_experience_level(resume, job_desc)` → Match result

## Data Models

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  last_login TIMESTAMP
);
```

#### Resumes Table
```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  original_filename VARCHAR(255) NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  file_size INTEGER NOT NULL,
  file_format VARCHAR(10) NOT NULL,  -- pdf, docx, txt
  text_content TEXT NOT NULL,
  parsed_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_deleted BOOLEAN DEFAULT FALSE
);
```

#### Resume Versions Table
```sql
CREATE TABLE resume_versions (
  id UUID PRIMARY KEY,
  resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
  version_number INTEGER NOT NULL,
  parsed_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by_action VARCHAR(50)  -- upload, edit, revert
);
```

#### Job Descriptions Table
```sql
CREATE TABLE job_descriptions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  company VARCHAR(255),
  content TEXT NOT NULL,
  parsed_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_deleted BOOLEAN DEFAULT FALSE
);
```

#### Analysis Results Table
```sql
CREATE TABLE analysis_results (
  id UUID PRIMARY KEY,
  resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
  job_id UUID NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
  ats_score FLOAT NOT NULL,
  score_breakdown JSONB NOT NULL,  -- keyword, formatting, skills, experience
  missing_keywords JSONB NOT NULL,
  formatting_issues JSONB NOT NULL,
  skill_gaps JSONB NOT NULL,
  recommendations JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Recommendations Table
```sql
CREATE TABLE recommendations (
  id UUID PRIMARY KEY,
  analysis_id UUID NOT NULL REFERENCES analysis_results(id) ON DELETE CASCADE,
  category VARCHAR(50) NOT NULL,
  priority INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  action TEXT NOT NULL,
  example TEXT,
  estimated_improvement FLOAT,
  user_accepted BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Audit Logs Table
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50) NOT NULL,
  resource_id UUID,
  details JSONB,
  ip_address VARCHAR(45),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Data Models (Python/Django)

```python
# User Model
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

# Resume Model
class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_size = models.IntegerField()
    file_format = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('docx', 'DOCX'), ('txt', 'TXT')])
    text_content = models.TextField()
    parsed_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

# Analysis Result Model
class AnalysisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    ats_score = models.FloatField()
    score_breakdown = models.JSONField()
    missing_keywords = models.JSONField()
    formatting_issues = models.JSONField()
    skill_gaps = models.JSONField()
    recommendations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```



## API Endpoints

### Authentication Endpoints

#### POST /api/auth/register
**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "full_name": "John Doe"
}
```
**Response** (201):
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "token": "jwt_token",
  "expires_in": 86400
}
```

#### POST /api/auth/login
**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```
**Response** (200):
```json
{
  "token": "jwt_token",
  "expires_in": 86400
}
```

#### POST /api/auth/refresh
**Request**: Headers with Authorization: Bearer {token}
**Response** (200):
```json
{
  "token": "new_jwt_token",
  "expires_in": 86400
}
```

#### POST /api/auth/password-reset
**Request**:
```json
{
  "email": "user@example.com"
}
```
**Response** (200):
```json
{
  "message": "Reset link sent to email"
}
```

### Resume Management Endpoints

#### POST /api/resumes/upload
**Request**: Multipart form data with file
**Response** (201):
```json
{
  "resume_id": "uuid",
  "filename": "resume.pdf",
  "file_size": 102400,
  "created_at": "2024-01-15T10:30:00Z",
  "parsed_data": { ... }
}
```

#### GET /api/resumes
**Response** (200):
```json
{
  "resumes": [
    {
      "id": "uuid",
      "filename": "resume.pdf",
      "created_at": "2024-01-15T10:30:00Z",
      "latest_ats_score": 78.5
    }
  ]
}
```

#### GET /api/resumes/{id}
**Response** (200):
```json
{
  "id": "uuid",
  "filename": "resume.pdf",
  "parsed_data": { ... },
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### DELETE /api/resumes/{id}
**Response** (204): No content

#### GET /api/resumes/{id}/versions
**Response** (200):
```json
{
  "versions": [
    {
      "version_id": "uuid",
      "version_number": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "ats_score": 78.5
    }
  ]
}
```

#### POST /api/resumes/{id}/revert
**Request**:
```json
{
  "version_id": "uuid"
}
```
**Response** (200):
```json
{
  "message": "Reverted to version 1",
  "current_version": 3
}
```

### Job Description Endpoints

#### POST /api/job-descriptions/upload
**Request**:
```json
{
  "title": "Senior Software Engineer",
  "company": "Tech Corp",
  "content": "Job description text..."
}
```
**Response** (201):
```json
{
  "job_id": "uuid",
  "title": "Senior Software Engineer",
  "parsed_data": { ... }
}
```

#### GET /api/job-descriptions
**Response** (200):
```json
{
  "jobs": [
    {
      "id": "uuid",
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Analysis Endpoints

#### POST /api/analysis/ats-score
**Request**:
```json
{
  "resume_id": "uuid",
  "job_id": "uuid"
}
```
**Response** (200):
```json
{
  "ats_score": 78.5,
  "score_breakdown": {
    "keyword_match": 85,
    "formatting": 70,
    "skill_alignment": 80,
    "experience_match": 75
  },
  "risk_level": "moderate",
  "missing_keywords": ["Python", "AWS", "Docker"],
  "formatting_issues": ["Multi-column layout detected"]
}
```

#### GET /api/analysis/recommendations/{resumeId}/{jobId}
**Response** (200):
```json
{
  "recommendations": [
    {
      "id": "uuid",
      "category": "keyword",
      "priority": 1,
      "title": "Add Python keyword",
      "description": "Python appears 5 times in job description",
      "action": "Add 'Python' to skills section",
      "example": "Skills: Python, JavaScript, Go",
      "estimated_improvement": 5.2
    }
  ]
}
```

#### GET /api/analysis/skill-gaps/{resumeId}/{jobId}
**Response** (200):
```json
{
  "skill_gaps": {
    "must_have": ["Kubernetes", "Docker"],
    "nice_to_have": ["Terraform", "Ansible"],
    "matched_skills": ["Python", "AWS"],
    "transferable_skills": ["Leadership", "Project Management"]
  }
}
```

#### GET /api/analysis/formatting/{resumeId}
**Response** (200):
```json
{
  "formatting_issues": [
    {
      "issue": "Multi-column layout",
      "severity": "high",
      "recommendation": "Convert to single-column layout",
      "impact": "May cause parsing errors"
    }
  ]
}
```

#### GET /api/analysis/benchmarking/{resumeId}
**Response** (200):
```json
{
  "benchmarking": {
    "keyword_percentile": 75,
    "skill_percentile": 82,
    "experience_percentile": 68,
    "overall_percentile": 75
  }
}
```



## NLP/ML Pipeline

### Resume Parsing Pipeline

**Input**: Resume file (PDF, DOCX, TXT)
**Output**: Structured resume data (JSON)

**Process**:
1. **File Extraction**: Extract text from file format
   - PDF: Use PyPDF2 or pdfplumber
   - DOCX: Use python-docx
   - TXT: Direct text reading

2. **Text Preprocessing**:
   - Remove extra whitespace
   - Normalize line breaks
   - Handle special characters
   - Detect encoding issues

3. **Section Detection**:
   - Identify resume sections (Contact, Experience, Education, Skills)
   - Use regex patterns and spaCy NER
   - Handle variations in section naming

4. **Data Extraction**:
   - Contact Information: Name, email, phone, location
   - Work Experience: Job title, company, dates, descriptions
   - Education: Degree, institution, graduation date, GPA
   - Skills: Technical skills, soft skills, certifications

5. **Date Normalization**:
   - Parse various date formats
   - Normalize to YYYY-MM-DD
   - Handle "Present" as current date

6. **Validation**:
   - Verify required fields present
   - Check data consistency
   - Flag missing or ambiguous sections

### Keyword Extraction Pipeline

**Input**: Resume text or job description
**Output**: Ranked keywords with scores

**Process**:
1. **Tokenization**: Use spaCy to tokenize text
2. **POS Tagging**: Identify parts of speech
3. **NER**: Extract named entities (organizations, locations, technologies)
4. **TF-IDF**: Calculate term frequency-inverse document frequency
5. **Keyword Ranking**: Rank by relevance and frequency
6. **Categorization**: Classify as technical, soft skills, or industry terms

**Keyword Categories**:
- Technical Keywords: Programming languages, frameworks, tools
- Soft Skills: Communication, leadership, teamwork
- Industry Terms: Domain-specific terminology
- Certifications: Professional certifications

### Semantic Similarity Analysis

**Input**: Resume text and job description
**Output**: Similarity scores for different sections

**Process**:
1. **Embedding Generation**: Use sentence-transformers to generate embeddings
   - Model: all-MiniLM-L6-v2 or similar
   - Embeddings: 384-dimensional vectors

2. **Similarity Calculation**: Compute cosine similarity
   - Formula: similarity = (A · B) / (||A|| × ||B||)
   - Range: 0 (completely different) to 1 (identical)

3. **Section-Level Analysis**:
   - Compare each work experience entry with job description
   - Compare skills section with required skills
   - Compare summary with job requirements

4. **Relevance Scoring**:
   - Score > 0.75: Highly relevant
   - Score 0.5-0.75: Moderately relevant
   - Score < 0.5: Low relevance

5. **Transferable Skills Identification**:
   - Find skills with high semantic similarity to required skills
   - Even if exact keyword match doesn't exist

### ATS Scoring Algorithm

**Input**: Resume, Job Description
**Output**: ATS Score (0-100)

**Scoring Components**:

1. **Keyword Match (40% weight)**
   - Count matching keywords between resume and job description
   - Formula: (matched_keywords / total_required_keywords) * 100
   - Considers both exact matches and semantic similarity

2. **Formatting Compliance (20% weight)**
   - Check for ATS-friendly formatting
   - Deduct points for:
     - Multi-column layouts (-20)
     - Excessive special characters (-15)
     - Inconsistent date formatting (-10)
     - Missing section headers (-10)
   - Formula: 100 - (total_deductions)

3. **Skill Alignment (25% weight)**
   - Match resume skills with required skills
   - Formula: (matched_skills / required_skills) * 100
   - Consider skill level if available

4. **Experience Match (15% weight)**
   - Compare years of experience
   - Formula: min(resume_years / required_years, 1.0) * 100
   - Penalize underqualification more than overqualification

**Final Score Calculation**:
```
ATS_Score = (
  keyword_match * 0.40 +
  formatting_score * 0.20 +
  skill_alignment * 0.25 +
  experience_match * 0.15
)
```

**Risk Level Classification**:
- Score >= 75: Low risk (likely to pass ATS)
- Score 60-74: Moderate risk (may pass ATS)
- Score < 60: High risk (likely to be filtered)

### Recommendation Generation

**Input**: Resume, Job Description, ATS Score, Analysis Results
**Output**: Prioritized recommendations

**Recommendation Categories**:

1. **Keyword Recommendations**
   - Identify missing high-frequency keywords
   - Suggest placement in resume
   - Estimate score improvement

2. **Skill Recommendations**
   - Identify missing required skills
   - Categorize as must-have or nice-to-have
   - Suggest learning resources

3. **Formatting Recommendations**
   - Suggest layout improvements
   - Recommend date format standardization
   - Suggest section reorganization

4. **Experience Recommendations**
   - Suggest restructuring descriptions
   - Recommend adding quantifiable metrics
   - Suggest action verb improvements

**Prioritization Algorithm**:
- Priority = (impact_on_score * 0.6) + (frequency_in_job_desc * 0.3) + (ease_of_implementation * 0.1)
- Sort by priority descending



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Resume Parsing Round-Trip Consistency

*For any valid resume document, parsing the document to extract structured data, then printing that structured data back to a resume format, then parsing again SHALL produce equivalent structured data.*

**Validates: Requirements 3.9, 3.10**

**Rationale**: This property ensures that the resume parser and pretty printer are inverses of each other. If parsing is lossy or printing is incorrect, this property will fail. This is critical for data integrity when users edit and re-save resumes.

### Property 2: ATS Score Range Validity

*For any resume-job description pair, the calculated ATS score SHALL be a number between 0 and 100 inclusive.*

**Validates: Requirements 5.1**

**Rationale**: The ATS score must always be within the valid range. This property ensures the scoring algorithm never produces invalid scores due to calculation errors or edge cases.

### Property 3: ATS Score Component Weights Sum to 100

*For any ATS score calculation, the weighted sum of all scoring components (keyword match, formatting, skill alignment, experience match) SHALL equal 100 when each component is scored 0-100.*

**Validates: Requirements 5.2, 5.3, 5.4, 5.5**

**Rationale**: The scoring algorithm uses weighted components. This property ensures the weights are correctly applied and sum to 100%, preventing score inflation or deflation.

### Property 4: Risk Level Classification Consistency

*For any ATS score, the assigned risk level SHALL be consistent: scores >= 75 are low-risk, scores 60-74 are moderate-risk, scores < 60 are high-risk.*

**Validates: Requirements 5.9, 5.10, 5.11**

**Rationale**: Risk level classification must be deterministic and consistent. This property ensures the classification logic is correct and doesn't have edge case bugs.

### Property 5: Semantic Similarity Score Range

*For any pair of text inputs, the calculated semantic similarity score SHALL be between 0 and 1 inclusive.*

**Validates: Requirements 6.1, 6.4, 6.5, 6.6**

**Rationale**: Semantic similarity is measured as cosine similarity, which must be in [0, 1]. This property ensures the embedding and similarity calculation is correct.

### Property 6: Keyword Extraction Completeness

*For any document, the extracted keywords SHALL include all keywords that appear in the document with frequency >= 2 and are not in the stop word list.*

**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**

**Rationale**: Keyword extraction must be comprehensive. This property ensures no important keywords are missed due to algorithm bugs.

### Property 7: Missing Keywords Subset Property

*For any resume-job description pair, the list of missing keywords SHALL be a subset of the job description keywords that do not appear in the resume.*

**Validates: Requirements 7.6, 7.9**

**Rationale**: Missing keywords should only include keywords from the job description that aren't in the resume. This property ensures the missing keyword identification is correct.

### Property 8: Skill Gap Categorization Validity

*For any skill gap analysis, each skill SHALL be categorized as either must-have or nice-to-have, and the categorization SHALL be consistent across multiple analyses of the same job description.*

**Validates: Requirements 11.2**

**Rationale**: Skill categorization must be deterministic and consistent. This property ensures the categorization logic doesn't have non-deterministic behavior.

### Property 9: Experience Level Matching Consistency

*For any resume-job description pair, the experience level match result SHALL be one of: overqualified, underqualified, or appropriate-level, and SHALL be consistent across multiple analyses.*

**Validates: Requirements 12.4, 12.5, 12.6**

**Rationale**: Experience matching must be deterministic. This property ensures the matching logic is consistent and doesn't have edge case bugs.

### Property 10: Resume Version Immutability

*For any resume version, the parsed data and content of that version SHALL remain unchanged after creation, even if the current resume is modified.*

**Validates: Requirements 9.2**

**Rationale**: Resume versions must be immutable snapshots. This property ensures version history is preserved correctly and previous versions aren't accidentally modified.

### Property 11: Recommendation Priority Ordering

*For any set of recommendations, the recommendations SHALL be ordered by priority in descending order (highest priority first), and the priority of each recommendation SHALL be >= 0 and <= 100.*

**Validates: Requirements 8.7**

**Rationale**: Recommendations must be properly prioritized. This property ensures the prioritization algorithm produces valid, ordered results.

### Property 12: Formatting Issue Detection Consistency

*For any resume with formatting issues, the detected issues SHALL be consistent across multiple analyses of the same resume.*

**Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5, 10.6**

**Rationale**: Formatting detection must be deterministic. This property ensures the detection logic is consistent and doesn't have non-deterministic behavior.

### Property 13: JWT Token Validity

*For any JWT token generated by the authentication system, the token SHALL be valid for exactly 24 hours from generation, and SHALL be invalid after expiration.*

**Validates: Requirements 1.4, 1.6**

**Rationale**: JWT tokens must have correct expiration. This property ensures token generation and validation is correct.

### Property 14: Password Validation Consistency

*For any password input, the validation result SHALL be consistent: passwords with length >= 8 characters SHALL pass validation, passwords with length < 8 SHALL fail validation.*

**Validates: Requirements 1.3**

**Rationale**: Password validation must be deterministic. This property ensures the validation logic is correct and consistent.

### Property 15: Email Format Validation

*For any email string, the validation result SHALL be consistent: valid email formats SHALL pass validation, invalid formats SHALL fail validation.*

**Validates: Requirements 1.2**

**Rationale**: Email validation must be deterministic. This property ensures the validation logic correctly identifies valid and invalid email formats.

### Property 16: File Size Validation

*For any file upload, files <= 10MB SHALL be accepted, files > 10MB SHALL be rejected with a file size error.*

**Validates: Requirements 2.4**

**Rationale**: File size validation must be deterministic. This property ensures the size check is correct and consistent.

### Property 17: File Format Validation

*For any file upload, files with format PDF, DOCX, or TXT SHALL be accepted, files with other formats SHALL be rejected with a format error.*

**Validates: Requirements 2.5**

**Rationale**: File format validation must be deterministic. This property ensures only supported formats are accepted.

### Property 18: Resume Unique Identifier Generation

*For any two resume uploads, the assigned unique identifiers SHALL be different.*

**Validates: Requirements 2.6**

**Rationale**: Resume IDs must be unique. This property ensures the ID generation algorithm produces unique IDs for each resume.

### Property 19: Recommendation Estimate Improvement Validity

*For any recommendation, the estimated score improvement SHALL be between 0 and 100.*

**Validates: Requirements 8.9**

**Rationale**: Score improvement estimates must be valid. This property ensures the estimation algorithm produces realistic values.

### Property 20: Skill Match Percentage Validity

*For any skill matching analysis, the skill match percentage SHALL be between 0 and 100 inclusive.*

**Validates: Requirements 5.4**

**Rationale**: Skill match percentages must be valid. This property ensures the calculation produces valid percentages.



## Error Handling

### Error Categories

**Validation Errors** (400 Bad Request)
- Invalid email format
- Password too short
- File size exceeds limit
- Unsupported file format
- Malformed JSON request

**Authentication Errors** (401 Unauthorized)
- Missing JWT token
- Invalid JWT token
- Expired JWT token
- Invalid credentials

**Authorization Errors** (403 Forbidden)
- User accessing another user's resume
- User accessing another user's job description
- Insufficient permissions

**Not Found Errors** (404 Not Found)
- Resume not found
- Job description not found
- Analysis result not found

**Server Errors** (500 Internal Server Error)
- Database connection failure
- File storage failure
- NLP processing failure
- Unexpected exceptions

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_EMAIL_FORMAT",
    "message": "The provided email address is not valid",
    "details": {
      "field": "email",
      "value": "invalid-email"
    },
    "tracking_id": "error-uuid-12345"
  }
}
```

### Error Handling Strategy

1. **Input Validation**: Validate all inputs before processing
2. **Graceful Degradation**: Provide fallback options when possible
3. **User-Friendly Messages**: Return clear, actionable error messages
4. **Logging**: Log all errors with context for debugging
5. **Monitoring**: Alert administrators on critical errors
6. **Recovery**: Provide retry mechanisms for transient failures

## Security Measures

### Authentication & Authorization

- **JWT Tokens**: Stateless authentication with 24-hour expiration
- **Password Hashing**: bcrypt with salt for password storage
- **Token Refresh**: Refresh endpoint for extending sessions
- **HTTPS**: All communications encrypted with TLS 1.2+
- **CORS**: Restrict cross-origin requests to trusted domains

### Data Protection

- **Encryption at Rest**: Encrypt sensitive data in database
- **Encryption in Transit**: HTTPS for all API communications
- **Data Deletion**: Permanent deletion of user data within 30 days of request
- **Access Control**: Row-level security to prevent cross-user data access
- **Audit Logging**: Log all sensitive operations

### API Security

- **Rate Limiting**: 100 requests per minute per user
- **Input Sanitization**: Sanitize all user inputs to prevent injection attacks
- **CSRF Protection**: CSRF tokens for state-changing operations
- **SQL Injection Prevention**: Use parameterized queries
- **XSS Prevention**: Escape all user-generated content

### Compliance

- **GDPR**: Comply with data retention and deletion requirements
- **PCI DSS**: If handling payment information, comply with PCI standards
- **Data Privacy**: Don't use resume data for model training without consent

## Testing Strategy

### Unit Testing

**Scope**: Individual functions and methods
**Coverage**: Aim for 80%+ code coverage
**Tools**: pytest, unittest

**Test Categories**:
- Input validation (valid/invalid inputs)
- Business logic (calculations, transformations)
- Error handling (exception handling)
- Edge cases (boundary conditions, empty inputs)

**Example Unit Tests**:
- Test password validation with various lengths
- Test email validation with various formats
- Test ATS score calculation with known inputs
- Test keyword extraction with sample text
- Test date normalization with various formats

### Property-Based Testing

**Scope**: Universal properties that should hold for all inputs
**Tools**: Hypothesis (Python)
**Minimum Iterations**: 100 per property

**Properties to Test**:
1. Resume parsing round-trip (parse → print → parse)
2. ATS score range validity (0-100)
3. Semantic similarity range (0-1)
4. Keyword extraction completeness
5. Risk level classification consistency
6. JWT token expiration
7. Password validation consistency
8. Email validation consistency
9. File size validation
10. File format validation
11. Resume ID uniqueness
12. Recommendation priority ordering
13. Formatting issue detection consistency
14. Skill match percentage validity
15. Recommendation improvement estimate validity

**Test Configuration**:
- Minimum 100 iterations per property
- Use appropriate generators for each property
- Tag each test with property number and requirements reference
- Example tag: `Feature: ai-resume-optimizer, Property 1: Resume parsing round-trip`

### Integration Testing

**Scope**: Component interactions and end-to-end flows
**Tools**: pytest, Django test client

**Test Scenarios**:
- User registration → login → resume upload → analysis
- Resume upload → parsing → version creation
- Resume modification → version creation → score recalculation
- Resume-job pairing → analysis → recommendations
- Resume comparison → version history
- File upload with various formats
- API authentication and authorization
- Error handling and recovery

### Performance Testing

**Scope**: Response time and scalability
**Tools**: Locust, Apache JMeter

**Performance Targets**:
- Resume upload: < 5 seconds for 10MB files
- ATS analysis: < 3 seconds
- Recommendations: < 5 seconds
- API response: < 2 seconds under 100 concurrent requests
- Database queries: < 1 second for typical queries

**Load Testing**:
- Simulate 100 concurrent users
- Verify response times remain under targets
- Monitor database and memory usage
- Identify bottlenecks and optimize

### Security Testing

**Scope**: Authentication, authorization, data protection
**Tools**: OWASP ZAP, Burp Suite

**Test Cases**:
- SQL injection attempts
- XSS injection attempts
- CSRF attacks
- Unauthorized access attempts
- Token expiration and refresh
- Password reset flow security
- Data encryption verification
- Rate limiting enforcement

### UI/UX Testing

**Scope**: Frontend components and user flows
**Tools**: Jest, React Testing Library, Cypress

**Test Categories**:
- Component rendering
- User interactions (click, input, submit)
- Form validation
- Error message display
- Loading states
- Responsive design
- Accessibility (WCAG 2.1 AA)

## Deployment and Scalability

### Deployment Architecture

**Frontend**:
- Deploy to AWS S3 + CloudFront
- Build optimization (code splitting, minification)
- Environment-specific configurations

**Backend**:
- Deploy to AWS ECS (Elastic Container Service)
- Docker containerization
- Auto-scaling based on CPU/memory
- Load balancing with AWS ALB

**Database**:
- PostgreSQL on AWS RDS
- Multi-AZ deployment for high availability
- Automated backups
- Read replicas for scaling read operations

**Storage**:
- AWS S3 for resume files
- Versioning enabled
- Lifecycle policies for old versions
- Encryption enabled

**Caching**:
- Redis on AWS ElastiCache
- Session storage
- Query result caching
- Rate limiting counters

### Scalability Considerations

**Horizontal Scaling**:
- Stateless API servers (can add/remove instances)
- Load balancing across instances
- Database connection pooling
- Cache distribution

**Vertical Scaling**:
- Increase instance size for CPU-intensive operations
- Increase database instance size for large datasets
- Increase cache size for frequently accessed data

**Optimization**:
- Database indexing on frequently queried columns
- Query optimization and caching
- Asynchronous processing for long-running tasks
- CDN for static assets

### Monitoring and Observability

**Metrics**:
- API response times
- Error rates
- Database query times
- Cache hit rates
- CPU and memory usage
- File upload success rates

**Logging**:
- Centralized logging with CloudWatch or ELK
- Structured logging with JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Audit logging for sensitive operations

**Alerting**:
- Alert on error rate > 5%
- Alert on response time > 2 seconds
- Alert on database connection failures
- Alert on disk space > 80%
- Alert on memory usage > 85%

### Disaster Recovery

**Backup Strategy**:
- Daily database backups
- 30-day retention for backups
- Test restore procedures monthly
- Backup encryption

**Recovery Procedures**:
- RTO (Recovery Time Objective): 1 hour
- RPO (Recovery Point Objective): 1 hour
- Documented runbooks for common failures
- Regular disaster recovery drills



## Technology Stack

### Frontend

- **Framework**: React.js 18+
- **State Management**: Redux Toolkit
- **HTTP Client**: Axios
- **UI Components**: Material-UI or Tailwind CSS
- **Form Handling**: React Hook Form
- **Validation**: Zod or Yup
- **Build Tool**: Vite or Webpack
- **Testing**: Jest, React Testing Library, Cypress
- **Code Quality**: ESLint, Prettier

### Backend

- **Framework**: Django 4.2+
- **REST API**: Django REST Framework
- **Authentication**: djangorestframework-simplejwt
- **Database ORM**: Django ORM
- **Task Queue**: Celery with Redis
- **Caching**: Django cache framework with Redis
- **Testing**: pytest, pytest-django
- **Code Quality**: Black, Flake8, isort

### NLP/ML Libraries

- **Text Processing**: spaCy 3.5+
- **Semantic Analysis**: sentence-transformers
- **Machine Learning**: scikit-learn
- **PDF Processing**: PyPDF2 or pdfplumber
- **DOCX Processing**: python-docx
- **Date Parsing**: dateutil, arrow

### Database

- **Primary Database**: PostgreSQL 14+
- **Connection Pooling**: psycopg2-pool
- **Migrations**: Alembic or Django migrations
- **Full-Text Search**: PostgreSQL built-in (optional)

### Caching & Sessions

- **Cache Backend**: Redis 7+
- **Session Storage**: Redis
- **Rate Limiting**: Redis-based counters

### Cloud Services

- **Compute**: AWS ECS (Elastic Container Service)
- **Storage**: AWS S3
- **Database**: AWS RDS (PostgreSQL)
- **Cache**: AWS ElastiCache (Redis)
- **CDN**: AWS CloudFront
- **Load Balancing**: AWS Application Load Balancer
- **Monitoring**: AWS CloudWatch
- **Logging**: AWS CloudWatch Logs or ELK Stack

### DevOps & Deployment

- **Containerization**: Docker
- **Orchestration**: AWS ECS or Kubernetes
- **CI/CD**: GitHub Actions or GitLab CI
- **Infrastructure as Code**: Terraform or CloudFormation
- **Secrets Management**: AWS Secrets Manager

## Integration Points

### External Services

#### Email Service
- **Purpose**: Send password reset links, notifications
- **Provider**: AWS SES or SendGrid
- **Integration**: Django email backend
- **Configuration**: API keys in environment variables

#### Cloud Storage
- **Purpose**: Store resume files
- **Provider**: AWS S3
- **Integration**: boto3 library
- **Configuration**: AWS credentials, bucket name

#### OAuth Providers (Optional)
- **Purpose**: Social login
- **Providers**: LinkedIn, Google
- **Integration**: django-allauth or social-auth-app-django
- **Configuration**: OAuth credentials

### Internal Service Integration

#### NLP Pipeline
- **Integration**: Synchronous for small files, asynchronous for large files
- **Fallback**: Graceful degradation if NLP service fails
- **Caching**: Cache parsed results to avoid re-processing

#### Database
- **Connection**: Connection pooling with psycopg2
- **Transactions**: Use database transactions for data consistency
- **Migrations**: Version-controlled schema changes

#### Cache Layer
- **Session Storage**: Store JWT tokens in Redis
- **Query Caching**: Cache frequently accessed data
- **Rate Limiting**: Use Redis for rate limit counters

### API Integration

#### Frontend-Backend Communication
- **Protocol**: HTTPS REST API
- **Authentication**: JWT tokens in Authorization header
- **Error Handling**: Standardized error response format
- **Versioning**: API versioning in URL path (/api/v1/)

#### Third-Party API Integration
- **Error Handling**: Retry logic with exponential backoff
- **Timeouts**: Set appropriate timeouts for external calls
- **Monitoring**: Log all external API calls
- **Fallback**: Provide fallback behavior if external service fails

## Data Flow Diagrams

### Resume Upload and Analysis Flow

```
User Upload Resume
    ↓
API: POST /api/resumes/upload
    ↓
Resume Upload Manager
    ├─ Validate file (size, format)
    ├─ Store file in S3
    └─ Extract text content
    ↓
Resume Parser
    ├─ Parse contact info
    ├─ Parse experience
    ├─ Parse education
    └─ Parse skills
    ↓
Store in Database
    ├─ Create Resume record
    └─ Create Resume Version record
    ↓
Return to User
```

### ATS Analysis Flow

```
User Request Analysis
    ↓
API: POST /api/analysis/ats-score
    ↓
Retrieve Resume & Job Description
    ↓
Keyword Extractor
    ├─ Extract resume keywords
    └─ Extract job keywords
    ↓
Semantic Analyzer
    ├─ Generate embeddings
    └─ Calculate similarity scores
    ↓
ATS Scorer
    ├─ Calculate keyword match (40%)
    ├─ Calculate formatting score (20%)
    ├─ Calculate skill alignment (25%)
    └─ Calculate experience match (15%)
    ↓
Recommendation Engine
    ├─ Generate recommendations
    ├─ Prioritize recommendations
    └─ Estimate improvements
    ↓
Store Analysis Results
    ↓
Return to User
```

### Resume Comparison Flow

```
User Request Comparison
    ↓
API: GET /api/resumes/{id}/versions
    ↓
Retrieve Version History
    ↓
Resume Comparison Engine
    ├─ Identify differences
    ├─ Calculate score changes
    └─ Highlight improvements
    ↓
Return Comparison to User
```



## Design Decisions and Rationale

### 1. Microservices vs Monolithic Architecture

**Decision**: Monolithic architecture with service-oriented design

**Rationale**:
- Simpler deployment and operational overhead
- Easier debugging and monitoring
- Sufficient for initial scale
- Can evolve to microservices later if needed
- Service-oriented design allows future separation

### 2. Synchronous vs Asynchronous Processing

**Decision**: Synchronous for small operations, asynchronous for long-running tasks

**Rationale**:
- Resume parsing: Asynchronous (can take 5+ seconds)
- ATS analysis: Synchronous (< 3 seconds target)
- Recommendations: Synchronous (< 5 seconds target)
- Email notifications: Asynchronous (non-blocking)

### 3. Caching Strategy

**Decision**: Multi-level caching with Redis

**Rationale**:
- Cache parsed resume data (1 hour TTL)
- Cache job description data (1 hour TTL)
- Cache analysis results (24 hour TTL)
- Cache keyword databases (7 day TTL)
- Reduces database load and improves response times

### 4. NLP Model Selection

**Decision**: Use pre-trained models (spaCy, sentence-transformers)

**Rationale**:
- Faster time to market
- No need for training data
- Proven performance on resume/job description data
- Can fine-tune later if needed
- Reduces infrastructure complexity

### 5. Database Schema Design

**Decision**: Normalized schema with JSONB for flexible data

**Rationale**:
- JSONB for parsed resume/job data (flexible structure)
- Relational tables for core entities (users, resumes, jobs)
- Audit logs for compliance and debugging
- Version history for tracking changes

### 6. API Design

**Decision**: RESTful API with JWT authentication

**Rationale**:
- Standard, well-understood approach
- Stateless authentication (scalable)
- Easy to test and document
- Compatible with frontend frameworks
- Can add GraphQL later if needed

### 7. File Storage

**Decision**: AWS S3 for resume files

**Rationale**:
- Scalable and reliable
- Automatic versioning support
- Encryption at rest
- Cost-effective for large files
- Easy integration with Django

### 8. Error Handling

**Decision**: Standardized error response format with tracking IDs

**Rationale**:
- Consistent error handling across API
- Tracking IDs for debugging
- User-friendly error messages
- Detailed error information for developers
- Facilitates monitoring and alerting

### 9. Security Approach

**Decision**: Defense in depth with multiple layers

**Rationale**:
- JWT for stateless authentication
- bcrypt for password hashing
- HTTPS for all communications
- Row-level security for data access
- Audit logging for compliance
- Rate limiting to prevent abuse

### 10. Testing Strategy

**Decision**: Combination of unit, property-based, integration, and performance tests

**Rationale**:
- Unit tests for individual functions
- Property-based tests for universal properties
- Integration tests for component interactions
- Performance tests for scalability
- Security tests for vulnerability detection

## Future Enhancements

### Phase 2 Features

1. **Advanced Analytics**
   - Track resume optimization progress over time
   - Identify trends in missing keywords
   - Provide personalized recommendations

2. **Resume Templates**
   - Provide ATS-friendly resume templates
   - Guide users through resume creation
   - Ensure formatting compliance

3. **Job Matching**
   - Recommend jobs based on resume
   - Track application history
   - Provide job market insights

4. **Collaboration Features**
   - Share resumes with mentors/coaches
   - Get feedback on resumes
   - Collaborative editing

5. **Mobile App**
   - React Native mobile application
   - On-the-go resume management
   - Push notifications for recommendations

### Phase 3 Features

1. **AI-Powered Resume Writing**
   - Generate resume content suggestions
   - Improve writing quality
   - Suggest action verbs and metrics

2. **Interview Preparation**
   - Practice interview questions
   - Get feedback on answers
   - Track interview performance

3. **Career Path Planning**
   - Identify career progression opportunities
   - Recommend skill development paths
   - Track career goals

4. **Marketplace Integration**
   - Connect with job boards
   - Direct job applications
   - Employer partnerships

## Assumptions and Constraints

### Assumptions

1. Users have valid email addresses
2. Resume files are in supported formats (PDF, DOCX, TXT)
3. Job descriptions are in English
4. Users have stable internet connection
5. Resume content is accurate and truthful

### Constraints

1. **File Size**: Maximum 10MB per resume
2. **Processing Time**: ATS analysis must complete within 3 seconds
3. **Concurrent Users**: System must support 100+ concurrent users
4. **Data Retention**: User data retained for 30 days after deletion request
5. **Availability**: Target 99.9% uptime
6. **Compliance**: Must comply with GDPR and data privacy regulations

## Success Metrics

### User Engagement

- User registration rate
- Resume upload rate
- Analysis request rate
- Recommendation acceptance rate
- User retention rate

### System Performance

- API response time (target: < 2 seconds)
- Resume parsing time (target: < 5 seconds)
- ATS analysis time (target: < 3 seconds)
- System uptime (target: 99.9%)
- Error rate (target: < 1%)

### Business Metrics

- User satisfaction score (target: > 4.5/5)
- Resume optimization success rate
- Job application success rate
- Customer acquisition cost
- Customer lifetime value

