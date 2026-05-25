# ResumeIQ - MVP Edition

##  Project Overview

The ResumeIQ MVP is a web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS). The MVP focuses on core functionality with a clean, user-friendly interface.

**Status**:  Backend Complete |  Ready for Frontend Development

---

##  What's Included

###  Backend (Production Ready)

1. **Authentication Module**
   - User registration and login
   - JWT token management
   - Password reset
   - User profile management

2. **Resume Management**
   - Resume upload (PDF, DOCX, TXT)
   - Text extraction and parsing
   - Structured data extraction
   - Version tracking

3. **ATS Scoring Engine**
   - Keyword matching (30%)
   - Skills matching (25%)
   - Resume structure (20%)
   - Experience matching (15%)
   - Grammar quality (10%)
   - Risk level classification
   - Missing keywords identification
   - Skill gaps identification

4. **Backend Infrastructure**
   - Django REST Framework
   - PostgreSQL database
   - JWT authentication
   - CORS configuration
   - Environment management

###  Frontend (To Be Built)

1. **Pages**
   - Login page
   - Register page
   - Dashboard page
   - Resume upload page
   - Results page

2. **Features**
   - User authentication
   - Resume management
   - Job description management
   - ATS analysis results
   - Responsive design

###  Deployment (Ready to Configure)

1. **Frontend**: Vercel
2. **Backend**: Render or Railway
3. **Database**: PostgreSQL

---



---

##  Documentation

### Quick Start
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Quick reference card with commands and endpoints

### MVP Planning
- **[MVP_SPECIFICATION.md](./MVP_SPECIFICATION.md)** - Complete MVP specification
- **[MVP_TASKS.md](./MVP_TASKS.md)** - Detailed task breakdown
- **[MVP_IMPLEMENTATION_SUMMARY.md](./MVP_IMPLEMENTATION_SUMMARY.md)** - Implementation summary

### Development Guides
- **[FRONTEND_QUICKSTART.md](./FRONTEND_QUICKSTART.md)** - Frontend development guide
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Deployment instructions

### Module Documentation
- **[FROZEN_MODULES.md](./FROZEN_MODULES.md)** - Frozen module documentation
- **[AUTHENTICATION_COMPLETE.md](./AUTHENTICATION_COMPLETE.md)** - Authentication details
- **[ATS_SCORING_SERVICE_IMPLEMENTATION.md](./backend/ATS_SCORING_SERVICE_IMPLEMENTATION.md)** - ATS scoring details

---

##  Getting Started

### Prerequisites
- Node.js 16+ and npm
- Python 3.11+
- Git
- PostgreSQL (for production)

### Backend Setup (Already Complete)

The backend is production-ready. To run locally:

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### Frontend Setup (To Be Done)

```bash
# Create React project
npm create vite@latest frontend -- --template react
cd frontend

# Install dependencies
npm install
npm install react-router-dom axios react-hook-form tailwindcss

# Configure Tailwind
npx tailwindcss init -p

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

##  API Endpoints

### Authentication
```
POST   /api/auth/register          - Register new user
POST   /api/auth/login             - Login user
POST   /api/auth/refresh           - Refresh JWT token
```

### Resumes
```
POST   /api/resumes/upload         - Upload resume
GET    /api/resumes                - List resumes
DELETE /api/resumes/{id}           - Delete resume
```

### Job Descriptions
```
POST   /api/job-descriptions/upload - Upload job description
GET    /api/job-descriptions        - List job descriptions
DELETE /api/job-descriptions/{id}   - Delete job description
```

### Analysis
```
POST   /api/analysis/ats/calculate_score - Calculate ATS score
GET    /api/analysis/ats/{id}            - Get analysis results
```

---

##  Frontend Pages

### 1. Login Page (`/login`)
- Email and password input
- Submit button
- Link to register page
- Error message display

### 2. Register Page (`/register`)
- Email, password, full name input
- Submit button
- Link to login page
- Error message display

### 3. Dashboard Page (`/dashboard`)
- List of uploaded resumes
- List of job descriptions
- Recent analysis results
- Upload buttons

### 4. Resume Upload Page (`/upload-resume`)
- Drag-and-drop upload area
- File validation
- Upload progress
- Parsed data display

### 5. Results Page (`/results/{resumeId}/{jobId}`)
- ATS score display (0-100)
- Score breakdown (5 components)
- Missing keywords (top 10)
- Skill gaps (top 10)
- Risk level indicator

---

##  ATS Scoring

### Scoring Components
| Component | Weight | Description |
|-----------|--------|-------------|
| Keyword Match | 30% | Keywords from job description found in resume |
| Skills Match | 25% | Required skills found in resume |
| Resume Structure | 20% | Formatting and section organization |
| Experience Match | 15% | Years of experience alignment |
| Grammar Quality | 10% | Writing quality and consistency |

### Risk Levels
- **Low Risk** (≥75): Resume likely to pass ATS
- **Moderate Risk** (60-74): Resume may pass ATS
- **High Risk** (<60): Resume likely to be filtered

---

##  Technology Stack

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT
- **NLP**: spaCy
- **Language**: Python 3.11

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **Routing**: React Router
- **HTTP Client**: Axios
- **Forms**: React Hook Form
- **Styling**: TailwindCSS

### Deployment
- **Frontend**: Vercel
- **Backend**: Render or Railway
- **Database**: PostgreSQL (managed)

---

##  Development Timeline

### Phase 1: Frontend Development (3-4 days)
- React project setup
- All pages implementation
- API integration
- Testing

### Phase 2: Deployment (1-2 days)
- Vercel configuration
- Render/Railway configuration
- PostgreSQL setup
- Environment configuration

**Total**: 4-6 days to MVP launch

---

##  Success Criteria

- ✅ Users can register and login
- ✅ Users can upload resumes
- ✅ Users can upload job descriptions
- ✅ Users can view ATS analysis results
- ✅ Dashboard displays all user data
- ✅ Results page shows detailed score breakdown
- ✅ Frontend connects to backend APIs
- ✅ Frontend deployed on Vercel
- ✅ Backend deployed on Render/Railway
- ✅ Database deployed on PostgreSQL
- ✅ All pages are responsive
- ✅ Error handling works correctly
- ✅ Loading states display properly

---

##  Frozen Modules (Do NOT Modify)

The following modules are production-ready and frozen:

1. **Authentication Module** (`backend/apps/users/`)
   - All tests passing
   - Production ready
   - Do NOT modify

2. **Resume Management** (`backend/apps/resumes/`)
   - All tests passing
   - Production ready
   - Do NOT modify

3. **ATS Scoring Engine** (`backend/apps/analysis/`)
   - 34 tests passing
   - Production ready
   - Do NOT modify

4. **Backend Infrastructure** (`backend/config/`)
   - All tests passing
   - Production ready
   - Do NOT modify

---

##  How to Use This Documentation

### For Frontend Development
1. Start with **[FRONTEND_QUICKSTART.md](./FRONTEND_QUICKSTART.md)**
2. Reference **[MVP_SPECIFICATION.md](./MVP_SPECIFICATION.md)** for page details
3. Use **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** for API endpoints

### For Deployment
1. Follow **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**
2. Reference **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** for environment variables

### For Understanding the Project
1. Read **[MVP_IMPLEMENTATION_SUMMARY.md](./MVP_IMPLEMENTATION_SUMMARY.md)**
2. Review **[FROZEN_MODULES.md](./FROZEN_MODULES.md)**
3. Check **[MVP_TASKS.md](./MVP_TASKS.md)** for remaining work

---

##  Key Concepts

### JWT Authentication
- User logs in with email/password
- Backend returns JWT token
- Frontend stores token in localStorage
- Token sent with each API request
- Token refreshed when expired

### ATS Scoring
- Resume and job description are analyzed
- 5 scoring components calculated
- Scores weighted and combined
- Risk level assigned
- Missing keywords and skills identified

### Resume Parsing
- Resume file uploaded
- Text extracted from file
- Text parsed into structured data
- Contact info, experience, education, skills extracted
- Data stored in database

---

##  Troubleshooting

### Frontend Issues
- **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in backend
- **API calls failing**: Check `VITE_API_URL` environment variable
- **Blank page**: Check browser console for errors

### Backend Issues
- **Database connection error**: Verify `DATABASE_URL`
- **500 errors**: Check backend logs
- **Authentication failing**: Verify JWT configuration

### Deployment Issues
- **Frontend not loading**: Check Vercel deployment logs
- **Backend not responding**: Check Render/Railway logs
- **Database not connecting**: Verify PostgreSQL connection string

---

## Support

### Documentation
- [MVP Specification](./MVP_SPECIFICATION.md)
- [Frontend Quickstart](./FRONTEND_QUICKSTART.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Quick Reference](./QUICK_REFERENCE.md)

### External Resources
- [React Documentation](https://react.dev)
- [Django Documentation](https://docs.djangoproject.com)
- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)

---

##  Ready to Launch

The ResumeIQ MVP is ready for frontend development and deployment. All backend modules are production-ready and frozen. Follow the guides in this documentation to complete the frontend and deploy to production.


**Let's build! **

---

##  Project Structure

```
AI-Resume-Optimizer/
├── backend/
│   ├── apps/
│   │   ├── users/          ✅ Authentication (Frozen)
│   │   ├── resumes/        ✅ Resume Management (Frozen)
│   │   ├── jobs/           ✅ Job Management (Frozen)
│   │   └── analysis/       ✅ ATS Scoring (Frozen)
│   ├── config/             ✅ Infrastructure (Frozen)
│   ├── manage.py
│   └── requirements.txt
├── frontend/                To Be Created
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   └── hooks/
│   ├── vite.config.js
│   └── package.json
├── docs/
│   ├── MVP_SPECIFICATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── FRONTEND_QUICKSTART.md
│   └── ...
└── README_MVP.md            This File
```

---

##  Next Steps

1. **Read** [FRONTEND_QUICKSTART.md](./FRONTEND_QUICKSTART.md)
2. **Create** React project
3. **Implement** all frontend pages
4. **Test** API integration
5. **Deploy** to Vercel and Render/Railway
6. **Launch** MVP

---

**Good luck! **

