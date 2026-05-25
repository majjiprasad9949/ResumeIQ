# ResumeIQ - Backend

Django REST Framework backend for the ResumeIQ + ATS Simulator application.

## Project Structure

```
backend/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── __init__.py
├── apps/                  # Django applications
│   ├── users/             # User authentication and profiles
│   ├── resumes/           # Resume upload and management
│   ├── jobs/              # Job description management
│   ├── analysis/          # ATS scoring and recommendations
│   ├── ai/                # NLP and ML models
│   └── utils/             # Utility models and helpers
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for Celery)
- pip

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Download NLP models**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## Apps Overview

### Users App (`apps/users/`)
- User registration and authentication
- User profile management
- JWT token handling

**Models:**
- `CustomUser`: Extended Django User model
- `UserProfile`: Additional user information

**Endpoints:**
- `POST /api/users/` - Register new user
- `GET /api/users/me/` - Get current user
- `PUT /api/users/update_profile/` - Update profile
- `POST /api/users/change_password/` - Change password

### Resumes App (`apps/resumes/`)
- Resume upload and storage
- Resume parsing and data extraction
- Resume versioning

**Models:**
- `Resume`: Main resume document
- `ResumeVersion`: Version history
- `ParsedResume`: Extracted structured data

**Endpoints:**
- `POST /api/resumes/` - Upload resume
- `GET /api/resumes/` - List resumes
- `GET /api/resumes/{id}/` - Get resume details
- `DELETE /api/resumes/{id}/` - Delete resume
- `GET /api/resumes/{id}/versions/` - Get versions
- `POST /api/resumes/{id}/revert/` - Revert to version

### Jobs App (`apps/jobs/`)
- Job description upload and management
- Job parsing and analysis

**Models:**
- `JobDescription`: Job posting document
- `ParsedJobDescription`: Extracted job data
- `ResumeJobPairing`: Resume-job associations

**Endpoints:**
- `POST /api/jobs/` - Upload job description
- `GET /api/jobs/` - List job descriptions
- `GET /api/jobs/{id}/` - Get job details
- `POST /api/jobs/{id}/pair_with_resume/` - Create pairing

### Analysis App (`apps/analysis/`)
- ATS scoring and simulation
- Recommendation generation
- Skill gap analysis

**Models:**
- `ATSAnalysis`: ATS score results
- `Recommendation`: Optimization suggestions
- `SkillGapAnalysis`: Skill gap data
- `FormattingIssue`: Formatting problems

**Endpoints:**
- `GET /api/analysis/ats/` - List analyses
- `GET /api/analysis/ats/{id}/` - Get analysis details
- `POST /api/analysis/ats/{id}/accept_recommendation/` - Accept recommendation
- `POST /api/analysis/ats/{id}/implement_recommendation/` - Mark as implemented

### AI App (`apps/ai/`)
- NLP model management
- Keyword extraction
- Semantic similarity analysis

**Models:**
- `KeywordExtraction`: Extracted keywords
- `SemanticSimilarity`: Similarity scores
- `NLPModel`: Model tracking

### Utils App (`apps/utils/`)
- System logging
- Audit logging
- Performance metrics

**Models:**
- `SystemLog`: System-wide logs
- `AuditLog`: User action logs
- `SystemMetric`: Performance metrics

## API Authentication

All endpoints (except registration and login) require JWT authentication.

### Getting a Token

```bash
POST /api/auth/token/
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token

Include in request header:
```
Authorization: Bearer <access_token>
```

### Refreshing Token

```bash
POST /api/auth/token/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Database Schema

### Key Tables

- **auth_user**: Django user accounts
- **users_customuser**: Extended user information
- **users_userprofile**: User profile data
- **resumes_resume**: Resume documents
- **resumes_resumeversion**: Resume versions
- **resumes_parsedresume**: Parsed resume data
- **jobs_jobdescription**: Job postings
- **jobs_parsedjobdescription**: Parsed job data
- **jobs_resumejobpairing**: Resume-job associations
- **analysis_atsanalysis**: ATS analysis results
- **analysis_recommendation**: Recommendations
- **analysis_skillgapanalysis**: Skill gaps
- **analysis_formattingissue**: Formatting issues

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Django secret key
- `DB_*`: Database credentials
- `CORS_ALLOWED_ORIGINS`: Allowed frontend origins
- `SPACY_MODEL`: spaCy model to use
- `SENTENCE_TRANSFORMER_MODEL`: Sentence transformer model

### Database Setup

```bash
# Create database
createdb ai_resume_optimizer

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Update `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Configure email service
- [ ] Set up Redis for Celery
- [ ] Configure S3 for file storage
- [ ] Run security checks: `python manage.py check --deploy`

### Using Gunicorn

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```bash
docker build -t ai-resume-optimizer-backend .
docker run -p 8000:8000 ai-resume-optimizer-backend
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
psql -U postgres -d ai_resume_optimizer

# Reset migrations
python manage.py migrate zero
python manage.py migrate
```

### NLP Model Issues

```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('OK')"
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping

# Start Redis (if not running)
redis-server
```

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests
4. Submit pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
