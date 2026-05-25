# Backend Project Structure

## Directory Layout

```
backend/
├── config/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                 # Main Django settings
│   ├── urls.py                     # URL routing configuration
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application (for async)
│
├── apps/                           # Django applications
│   ├── __init__.py
│   │
│   ├── users/                      # User authentication & profiles
│   │   ├── __init__.py
│   │   ├── apps.py                # App configuration
│   │   ├── models.py              # CustomUser, UserProfile
│   │   ├── views.py               # UserViewSet
│   │   ├── serializers.py         # User serializers
│   │   ├── urls.py                # User endpoints
│   │   ├── admin.py               # Admin configuration
│   │   ├── permissions.py         # Custom permissions
│   │   ├── authentication.py      # Auth utilities
│   │   └── migrations/            # Database migrations
│   │
│   ├── resumes/                    # Resume management
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # Resume, ResumeVersion, ParsedResume
│   │   ├── views.py               # ResumeViewSet
│   │   ├── serializers.py         # Resume serializers
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── parsers.py             # Resume parsing logic
│   │   ├── tasks.py               # Celery tasks
│   │   └── migrations/
│   │
│   ├── jobs/                       # Job description management
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # JobDescription, ParsedJobDescription
│   │   ├── views.py               # JobDescriptionViewSet
│   │   ├── serializers.py         # Job serializers
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── parsers.py             # Job parsing logic
│   │   ├── tasks.py               # Celery tasks
│   │   └── migrations/
│   │
│   ├── analysis/                   # ATS analysis & recommendations
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # ATSAnalysis, Recommendation, etc.
│   │   ├── views.py               # AnalysisViewSet
│   │   ├── serializers.py         # Analysis serializers
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── scoring.py             # ATS scoring logic
│   │   ├── recommendations.py     # Recommendation generation
│   │   ├── tasks.py               # Celery tasks
│   │   └── migrations/
│   │
│   ├── ai/                         # NLP & ML models
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # KeywordExtraction, SemanticSimilarity
│   │   ├── admin.py
│   │   ├── nlp_processor.py       # spaCy processing
│   │   ├── keyword_extractor.py   # Keyword extraction
│   │   ├── semantic_analyzer.py   # Semantic similarity
│   │   ├── skill_matcher.py       # Skill matching
│   │   ├── model_loader.py        # Model loading utilities
│   │   └── migrations/
│   │
│   └── utils/                      # Utilities & helpers
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py              # SystemLog, AuditLog, SystemMetric
│       ├── admin.py
│       ├── decorators.py          # Custom decorators
│       ├── middleware.py          # Custom middleware
│       ├── exceptions.py          # Custom exceptions
│       ├── validators.py          # Custom validators
│       ├── helpers.py             # Helper functions
│       ├── file_handlers.py       # File processing
│       ├── logging_utils.py       # Logging utilities
│       └── migrations/
│
├── static/                         # Static files (CSS, JS, images)
│   └── admin/
│
├── media/                          # User uploaded files
│   ├── resumes/
│   ├── resume_versions/
│   └── profile_pictures/
│
├── logs/                           # Application logs
│   └── django.log
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── test_users.py
│   ├── test_resumes.py
│   ├── test_jobs.py
│   ├── test_analysis.py
│   └── test_ai.py
│
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker compose configuration
├── README.md                       # Backend documentation
└── setup.py                        # Package setup (optional)
```

## App Responsibilities

### Users App
**Purpose**: User authentication, registration, and profile management

**Key Components**:
- User registration with email validation
- JWT token generation and refresh
- User profile management
- Password reset functionality
- User preferences and settings

**Database Tables**:
- `auth_user` (Django built-in)
- `users_customuser`
- `users_userprofile`

**API Endpoints**:
- `POST /api/users/` - Register
- `GET /api/users/me/` - Current user
- `PUT /api/users/update_profile/` - Update profile
- `POST /api/users/change_password/` - Change password

---

### Resumes App
**Purpose**: Resume upload, storage, parsing, and versioning

**Key Components**:
- Resume file upload (PDF, DOCX, TXT)
- Resume text extraction
- Resume parsing and data extraction
- Resume versioning and history
- Resume comparison

**Database Tables**:
- `resumes_resume`
- `resumes_resumeversion`
- `resumes_parsedresume`

**API Endpoints**:
- `POST /api/resumes/` - Upload resume
- `GET /api/resumes/` - List resumes
- `GET /api/resumes/{id}/` - Get details
- `DELETE /api/resumes/{id}/` - Delete
- `GET /api/resumes/{id}/versions/` - Get versions
- `POST /api/resumes/{id}/revert/` - Revert version

**Celery Tasks**:
- `parse_resume` - Extract resume data
- `extract_resume_text` - Get text from file
- `create_resume_version` - Version management

---

### Jobs App
**Purpose**: Job description upload, storage, and parsing

**Key Components**:
- Job description upload
- Job text extraction
- Job parsing and data extraction
- Resume-job pairing

**Database Tables**:
- `jobs_jobdescription`
- `jobs_parsedjobdescription`
- `jobs_resumejobpairing`

**API Endpoints**:
- `POST /api/jobs/` - Upload job
- `GET /api/jobs/` - List jobs
- `GET /api/jobs/{id}/` - Get details
- `POST /api/jobs/{id}/pair_with_resume/` - Create pairing

**Celery Tasks**:
- `parse_job_description` - Extract job data
- `extract_job_text` - Get text from file

---

### Analysis App
**Purpose**: ATS scoring, recommendations, and skill gap analysis

**Key Components**:
- ATS score calculation (keyword, formatting, skills, experience)
- Recommendation generation
- Skill gap analysis
- Formatting validation
- Experience level matching

**Database Tables**:
- `analysis_atsanalysis`
- `analysis_recommendation`
- `analysis_skillgapanalysis`
- `analysis_formattingissue`

**API Endpoints**:
- `GET /api/analysis/ats/` - List analyses
- `GET /api/analysis/ats/{id}/` - Get analysis
- `POST /api/analysis/ats/{id}/accept_recommendation/` - Accept
- `POST /api/analysis/ats/{id}/implement_recommendation/` - Implement

**Celery Tasks**:
- `calculate_ats_score` - Main scoring
- `generate_recommendations` - Generate suggestions
- `analyze_skill_gaps` - Skill analysis
- `validate_formatting` - Format checking

---

### AI App
**Purpose**: NLP processing and machine learning

**Key Components**:
- spaCy NLP processing
- Keyword extraction (TF-IDF)
- Semantic similarity (sentence-transformers)
- Skill matching (scikit-learn)
- Model management

**Database Tables**:
- `ai_keywordextraction`
- `ai_semanticsimilarity`
- `ai_nlpmodel`

**Key Modules**:
- `nlp_processor.py` - spaCy processing
- `keyword_extractor.py` - Keyword extraction
- `semantic_analyzer.py` - Semantic similarity
- `skill_matcher.py` - Skill matching
- `model_loader.py` - Model management

---

### Utils App
**Purpose**: System-wide utilities and helpers

**Key Components**:
- System logging
- Audit logging
- Performance metrics
- Custom decorators
- Custom middleware
- File handling utilities
- Validation utilities

**Database Tables**:
- `utils_systemlog`
- `utils_auditlog`
- `utils_systemmetric`

**Key Modules**:
- `logging_utils.py` - Logging setup
- `file_handlers.py` - File processing
- `validators.py` - Custom validators
- `decorators.py` - Custom decorators
- `middleware.py` - Custom middleware
- `exceptions.py` - Custom exceptions

---

## Data Flow

### Resume Upload Flow
```
1. User uploads resume file
2. ResumesViewSet.create() receives file
3. Resume model created with file
4. Celery task: parse_resume triggered
5. Resume text extracted
6. spaCy NLP processing
7. ParsedResume model populated
8. Parsing status updated
```

### ATS Analysis Flow
```
1. User requests analysis for resume + job
2. ResumeJobPairing created
3. Celery task: calculate_ats_score triggered
4. Keyword extraction for both documents
5. Semantic similarity calculation
6. Formatting validation
7. Experience matching
8. ATS score calculated
9. Recommendations generated
10. Results stored in database
```

### Recommendation Generation Flow
```
1. Analysis complete
2. Celery task: generate_recommendations triggered
3. Missing keywords identified
4. Skill gaps analyzed
5. Formatting issues detected
6. Experience mismatches found
7. Recommendations prioritized
8. Score improvement estimated
9. Recommendations stored
```

---

## Technology Stack

### Core Framework
- **Django 4.2.8** - Web framework
- **Django REST Framework 3.14.0** - REST API
- **djangorestframework-simplejwt 5.3.2** - JWT authentication

### Database
- **PostgreSQL 12+** - Primary database
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

### NLP & ML
- **spaCy 3.7.2** - NLP processing
- **sentence-transformers 2.2.2** - Semantic similarity
- **scikit-learn 1.3.2** - Machine learning

### File Processing
- **pdfplumber 0.10.3** - PDF extraction
- **python-docx 0.8.11** - DOCX extraction

### Async Tasks
- **Celery 5.3.4** - Task queue
- **Redis 5.0.1** - Message broker

### Development
- **pytest 7.4.3** - Testing framework
- **black 23.12.0** - Code formatter
- **flake8 6.1.0** - Linter

---

## Configuration Files

### settings.py
Main Django configuration with:
- Database settings
- Installed apps
- Middleware
- REST Framework configuration
- JWT settings
- CORS configuration
- File upload settings
- NLP model configuration
- Celery configuration
- Logging configuration
- Security settings

### urls.py
URL routing:
- Admin interface
- JWT token endpoints
- API endpoints for all apps

### .env.example
Environment variables template for:
- Django settings
- Database credentials
- JWT configuration
- Email settings
- NLP models
- Celery configuration
- AWS S3 (optional)
- Security settings

---

## Development Workflow

### Adding a New Feature

1. **Create models** in `apps/<app>/models.py`
2. **Create serializers** in `apps/<app>/serializers.py`
3. **Create views** in `apps/<app>/views.py`
4. **Add URLs** in `apps/<app>/urls.py`
5. **Create migrations**: `python manage.py makemigrations`
6. **Run migrations**: `python manage.py migrate`
7. **Write tests** in `tests/test_<app>.py`
8. **Add to admin** in `apps/<app>/admin.py`

### Running the Project

```bash
# Development server
python manage.py runserver

# With Celery worker
celery -A config worker -l info

# With Celery beat (scheduled tasks)
celery -A config beat -l info
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Revert migrations
python manage.py migrate <app> <migration_number>

# Create superuser
python manage.py createsuperuser

# Shell access
python manage.py shell
```

---

## Security Considerations

1. **Authentication**: JWT tokens with 24-hour expiration
2. **Authorization**: Role-based access control
3. **Data Protection**: HTTPS, bcrypt password hashing
4. **File Upload**: Validation of file types and sizes
5. **SQL Injection**: Django ORM prevents SQL injection
6. **CSRF Protection**: Django CSRF middleware
7. **Rate Limiting**: API rate limiting (to be implemented)
8. **Audit Logging**: All user actions logged

---

## Performance Optimization

1. **Database Indexing**: Indexes on frequently queried fields
2. **Caching**: Redis caching for NLP models
3. **Async Tasks**: Celery for long-running operations
4. **Pagination**: API pagination for large datasets
5. **Query Optimization**: Select_related and prefetch_related
6. **File Streaming**: Streaming for large file uploads

---

## Monitoring & Logging

1. **System Logs**: Application logs in `logs/django.log`
2. **Audit Logs**: User action tracking
3. **Performance Metrics**: API response times, database queries
4. **Error Tracking**: Exception logging and reporting
5. **Health Checks**: System health monitoring

---

## Deployment

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up monitoring
- [ ] Configure email service
- [ ] Set up Redis
- [ ] Configure S3 storage
- [ ] Run security checks

### Deployment Options
1. **Traditional Server**: Gunicorn + Nginx
2. **Docker**: Docker + Docker Compose
3. **Cloud**: AWS, Google Cloud, Heroku
4. **Kubernetes**: K8s deployment

---

## Next Steps

1. Implement resume parsing logic
2. Implement ATS scoring algorithm
3. Implement recommendation engine
4. Implement NLP processing
5. Add comprehensive tests
6. Set up CI/CD pipeline
7. Configure production deployment
8. Set up monitoring and alerting
