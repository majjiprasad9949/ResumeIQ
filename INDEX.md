# ResumeIQ - Project Index

## Project Overview

ResumeIQ + ATS Simulator is a comprehensive web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) using advanced NLP techniques and AI-powered recommendations.

**Tech Stack**: React.js + Django REST Framework + PostgreSQL + spaCy + sentence-transformers

---

## Documentation Index

### Getting Started
1. **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
   - Installation steps
   - Quick testing
   - Common tasks
   - Troubleshooting

2. **[README.md](backend/README.md)** - Backend setup guide
   - Installation instructions
   - Project structure
   - App descriptions
   - Configuration guide

### Authentication Module 

3. **[AUTHENTICATION_COMPLETE.md](AUTHENTICATION_COMPLETE.md)** - Complete implementation summary
   - What was built
   - Features implemented
   - Database schema
   - Security features
   - Testing coverage

4. **[AUTHENTICATION_API.md](backend/AUTHENTICATION_API.md)** - API documentation
   - All endpoints documented
   - Request/response examples
   - Error handling
   - Security considerations
   - Usage examples (JavaScript, Python)

5. **[AUTHENTICATION_TESTING.md](backend/AUTHENTICATION_TESTING.md)** - Testing guide
   - cURL examples
   - Postman setup
   - Python unit tests
   - Manual testing checklist
   - Performance testing
   - Debugging guide

6. **[AUTHENTICATION_IMPLEMENTATION.md](AUTHENTICATION_IMPLEMENTATION.md)** - Implementation details
   - Files created/modified
   - Features implemented
   - API endpoints
   - Database schema
   - Configuration
   - Installation steps

### Project Structure

7. **[BACKEND_STRUCTURE.md](BACKEND_STRUCTURE.md)** - Detailed project structure
   - Complete directory layout
   - App responsibilities
   - Data flow diagrams
   - Technology stack
   - Configuration details
   - Development workflow

8. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Phase 1 summary
   - Project overview
   - What was created
   - Project structure
   - Key features
   - Technology stack
   - Next steps

---

## File Structure

```
AI-Resume-Optimizer/
├── backend/                          # Django backend
│   ├── config/                       # Django project settings
│   │   ├── settings.py              # Main configuration
│   │   ├── urls.py                  # URL routing
│   │   └── wsgi.py                  # WSGI app
│   │
│   ├── apps/                        # Django applications
│   │   ├── users/                   # ✅ Authentication (COMPLETE)
│   │   │   ├── models.py            # 4 models
│   │   │   ├── serializers.py       # 10 serializers
│   │   │   ├── views.py             # UserViewSet
│   │   │   ├── urls.py              # Endpoints
│   │   │   ├── admin.py             # Admin interface
│   │   │   ├── permissions.py       # Custom permissions
│   │   │   ├── utils.py             # Helper functions
│   │   │   ├── signals.py           # Django signals
│   │   │   └── apps.py              # App config
│   │   │
│   │   ├── resumes/                 # Resume management (TODO)
│   │   ├── jobs/                    # Job management (TODO)
│   │   ├── analysis/                # ATS analysis (TODO)
│   │   ├── ai/                      # NLP processing (TODO)
│   │   └── utils/                   # System utilities (TODO)
│   │
│   ├── manage.py                    # Django CLI
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment template
│   ├── README.md                    # Backend documentation
│   ├── AUTHENTICATION_API.md        # API documentation
│   └── AUTHENTICATION_TESTING.md    # Testing guide
│
├── QUICK_START.md                   # Quick reference
├── AUTHENTICATION_COMPLETE.md       # Implementation summary
├── AUTHENTICATION_IMPLEMENTATION.md # Implementation details
├── BACKEND_STRUCTURE.md             # Project structure
├── IMPLEMENTATION_SUMMARY.md        # Phase 1 summary
└── INDEX.md                         # This file
```

---

## Phase Progress

### Phase 1: Backend Setup & Authentication ✅ COMPLETE
- ✅ Django project structure
- ✅ 6 apps created (users, resumes, jobs, analysis, ai, utils)
- ✅ Authentication module fully implemented
- ✅ JWT authentication configured
- ✅ Email verification implemented
- ✅ Password management implemented
- ✅ User profile management implemented
- ✅ Comprehensive documentation
- ✅ Testing guides

**Status**: Ready for frontend integration

### Phase 2: Resume Management ⏳ PENDING
- [ ] Resume upload (PDF, DOCX, TXT)
- [ ] Resume parsing and data extraction
- [ ] Resume versioning
- [ ] Resume comparison
- [ ] API endpoints

### Phase 3: Job Management ⏳ PENDING
- [ ] Job description upload
- [ ] Job parsing and analysis
- [ ] Resume-job pairing
- [ ] API endpoints

### Phase 4: Analysis & NLP ⏳ PENDING
- [ ] ATS scoring algorithm
- [ ] Recommendation engine
- [ ] Skill gap analysis
- [ ] Formatting validation
- [ ] Semantic similarity analysis
- [ ] Keyword extraction

### Phase 5: Frontend Integration ⏳ PENDING
- [ ] React authentication pages
- [ ] User dashboard
- [ ] Resume upload interface
- [ ] Analysis dashboard
- [ ] Recommendation display

### Phase 6: Testing & Deployment ⏳ PENDING
- [ ] Comprehensive testing
- [ ] CI/CD pipeline
- [ ] Production deployment
- [ ] Monitoring setup

---

## Quick Links

### Setup & Installation
- [Quick Start (5 min)](QUICK_START.md)
- [Backend README](backend/README.md)
- [Backend Structure](BACKEND_STRUCTURE.md)

### Authentication (Phase 1)
- [API Documentation](backend/AUTHENTICATION_API.md)
- [Testing Guide](backend/AUTHENTICATION_TESTING.md)
- [Implementation Details](AUTHENTICATION_IMPLEMENTATION.md)
- [Complete Summary](AUTHENTICATION_COMPLETE.md)

### API Endpoints

#### Authentication
```
POST   /api/users/register/                    - Register
POST   /api/users/auth/login/                  - Login
POST   /api/users/auth/refresh/                - Refresh token
POST   /api/users/logout/                      - Logout
```

#### User Profile
```
GET    /api/users/me/                          - Get current user
PUT    /api/users/update_profile/              - Update profile
PATCH  /api/users/update_profile/              - Partial update
```

#### Password Management
```
POST   /api/users/change_password/             - Change password
POST   /api/users/forgot_password/             - Request reset
POST   /api/users/reset_password/              - Reset password
```

#### Email Verification
```
POST   /api/users/verify_email/                - Verify email
POST   /api/users/resend_verification_email/   - Resend verification
```

---

## Technology Stack

### Backend
- **Framework**: Django 4.2.8
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt 5.3.2)
- **Database**: PostgreSQL 12+
- **ORM**: Django ORM

### NLP & ML
- **NLP**: spaCy 3.7.2
- **Embeddings**: sentence-transformers 2.2.2
- **ML**: scikit-learn 1.3.2

### File Processing
- **PDF**: pdfplumber 0.10.3
- **DOCX**: python-docx 0.8.11

### Async Processing
- **Task Queue**: Celery 5.3.4
- **Message Broker**: Redis 5.0.1

### Development
- **Testing**: pytest 7.4.3
- **Formatting**: black 23.12.0
- **Linting**: flake8 6.1.0

---

## Environment Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (for Celery)
- pip

### Quick Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

---

## Key Features

### Authentication ✅
- Email-based registration
- JWT token authentication
- Email verification
- Password reset
- User profile management
- Profile picture upload
- User preferences

### Security ✅
- Password hashing (bcrypt)
- JWT tokens with expiration
- Token blacklisting
- Email verification tokens
- Password reset tokens
- HTTPS support
- CORS configuration

### Admin Interface ✅
- User management
- Profile management
- Token management
- Statistics tracking

---

## Testing

### Quick Test
```bash
# Register
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!"
  }'

# Login
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'

# Get current user
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

### Full Testing
See [AUTHENTICATION_TESTING.md](backend/AUTHENTICATION_TESTING.md) for:
- cURL examples
- Postman setup
- Python unit tests
- Manual testing checklist

---

## Admin Panel

Access at: `http://localhost:8000/admin/`

**Manage:**
- Users
- User Profiles
- Password Reset Tokens
- Email Verification Tokens

---

## Troubleshooting

### Database Connection
```bash
psql -U postgres -d ai_resume_optimizer
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Email Not Sending
- Check EMAIL_BACKEND in .env
- For development, use console backend

### Token Issues
- Verify SECRET_KEY is set
- Check JWT settings in settings.py

---

## Support & Resources

### Documentation
- [Quick Start](QUICK_START.md)
- [API Documentation](backend/AUTHENTICATION_API.md)
- [Testing Guide](backend/AUTHENTICATION_TESTING.md)
- [Backend README](backend/README.md)
- [Project Structure](BACKEND_STRUCTURE.md)

### Tools
- Django Admin: `http://localhost:8000/admin/`
- API Root: `http://localhost:8000/api/`

### Debugging
- Django shell: `python manage.py shell`
- Logs: `logs/django.log`
- Database: `psql -U postgres -d ai_resume_optimizer`

---

## Next Steps

1. ✅ **Phase 1 Complete**: Authentication module ready
2. ⏳ **Phase 2**: Resume management module
3. ⏳ **Phase 3**: Job management module
4. ⏳ **Phase 4**: Analysis & NLP module
5. ⏳ **Phase 5**: Frontend integration
6. ⏳ **Phase 6**: Testing & deployment

---

## Project Status

**Current Phase**: Phase 1 - Authentication Module ✅ COMPLETE

**Ready For**:
- ✅ Frontend integration
- ✅ Testing
- ✅ Deployment
- ✅ Production use

**Next Phase**: Resume Management Module

---

## Contact & Support

For issues or questions:
1. Check documentation files
2. Review error messages
3. Check Django logs
4. Open GitHub issue

---

## License

MIT License

---

**Last Updated**: 2024
**Status**: Phase 1 Complete - Ready for Phase 2
**Version**: 1.0.0
