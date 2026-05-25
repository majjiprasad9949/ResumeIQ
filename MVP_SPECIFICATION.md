# ResumeIQ - MVP Specification

## Project Scope

This document defines the Minimum Viable Product (MVP) for the ResumeIQ. The MVP focuses on core functionality with a clean, user-friendly interface.

## Frozen Modules (Production Ready)

The following modules are complete and will NOT be modified:

### 1. Backend Infrastructure ✅
- Django REST Framework setup
- PostgreSQL database configuration
- JWT authentication system
- CORS configuration
- Environment management

### 2. Authentication Module ✅
- User registration with email validation
- User login with JWT tokens
- Token refresh mechanism
- Password reset flow
- User profile management

### 3. Resume Management Module ✅
- Resume file upload (PDF, DOCX, TXT)
- Resume text extraction
- Resume parsing and structured data extraction
- Resume versioning and history
- Resume deletion

### 4. ATS Scoring Engine ✅
- Keyword match scoring (30%)
- Skills match scoring (25%)
- Resume structure scoring (20%)
- Experience match scoring (15%)
- Grammar quality scoring (10%)
- Risk level classification
- Missing keywords identification
- Skill gaps identification

## MVP Features to Build

### 1. React Frontend

#### Technology Stack
- **Framework**: React 18+ with Vite
- **Routing**: React Router v6
- **Styling**: TailwindCSS
- **Forms**: React Hook Form
- **HTTP Client**: Axios
- **State Management**: React Context API (minimal)
- **Build Tool**: Vite

#### Pages

##### 1.1 Login Page
**URL**: `/login`
**Purpose**: User authentication

**Components**:
- Email input field
- Password input field
- "Remember me" checkbox (optional)
- Login button
- "Don't have an account? Register" link
- Error message display
- Loading state during submission

**Functionality**:
- Form validation (email format, password length)
- Submit login credentials to backend
- Store JWT token in localStorage
- Redirect to dashboard on success
- Display error messages on failure

**API Call**:
```
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

---

##### 1.2 Register Page
**URL**: `/register`
**Purpose**: New user registration

**Components**:
- Full name input field
- Email input field
- Password input field
- Confirm password input field
- Register button
- "Already have an account? Login" link
- Error message display
- Loading state during submission

**Functionality**:
- Form validation (email format, password strength, password match)
- Submit registration data to backend
- Auto-login after successful registration
- Redirect to dashboard
- Display error messages on failure

**API Call**:
```
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

---

##### 1.3 Resume Upload Page
**URL**: `/upload-resume`
**Purpose**: Upload and parse resume

**Components**:
- Drag-and-drop upload area
- File input button
- File name display
- File size display
- Upload progress bar
- Cancel upload button
- Parsed resume data display (after upload)
- Back to dashboard button

**Functionality**:
- Accept PDF, DOCX, TXT files
- Validate file size (max 10MB)
- Show upload progress
- Display parsed resume data:
  - Contact information
  - Work experience
  - Education
  - Skills
  - Certifications
- Allow user to confirm and save
- Redirect to dashboard after save

**API Call**:
```
POST /api/resumes/upload
Content-Type: multipart/form-data
{
  "file": <file>,
  "title": "My Resume"
}
```

---

##### 1.4 Dashboard Page
**URL**: `/dashboard`
**Purpose**: Main hub for resume and job management

**Components**:
- Welcome message with user name
- "Upload Resume" button
- "Upload Job Description" button
- Resumes section:
  - List of uploaded resumes
  - Resume title
  - Upload date
  - Delete button
  - View results button
- Job Descriptions section:
  - List of uploaded job descriptions
  - Job title
  - Company name
  - Upload date
  - Delete button
- Recent Analysis Results:
  - Resume title
  - Job title
  - ATS score
  - Risk level indicator
  - View details button

**Functionality**:
- Display all user's resumes
- Display all user's job descriptions
- Show latest analysis results
- Allow resume deletion with confirmation
- Allow job description deletion with confirmation
- Navigate to upload pages
- Navigate to results page

**API Calls**:
```
GET /api/resumes
GET /api/job-descriptions
DELETE /api/resumes/{id}
DELETE /api/job-descriptions/{id}
```

---

##### 1.5 Results Page
**URL**: `/results/{resumeId}/{jobId}`
**Purpose**: Display ATS analysis results

**Components**:
- Resume title and job title display
- Overall ATS score display (large, centered)
  - Visual indicator (gauge or progress bar)
  - Score out of 100
  - Risk level badge (Low/Moderate/High)
- Score breakdown section:
  - Keyword Match: 30% (with score)
  - Skills Match: 25% (with score)
  - Resume Structure: 20% (with score)
  - Experience Match: 15% (with score)
  - Grammar Quality: 10% (with score)
  - Each with visual bar
- Missing Keywords section:
  - List of top 10 missing keywords
  - Frequency indicator
- Skill Gaps section:
  - List of top 10 missing skills
  - Categorization (must-have/nice-to-have if available)
- Back to dashboard button
- Download report button (optional)

**Functionality**:
- Fetch analysis results from backend
- Display all score components
- Show visual indicators for scores
- Display missing keywords and skill gaps
- Allow user to go back to dashboard
- Allow user to download results as PDF (optional)

**API Call**:
```
GET /api/analysis/ats/{analysisId}
```

---

#### 1.6 Navigation and Layout

**Main Layout Component**:
- Header with logo
- Navigation bar with:
  - Dashboard link
  - Upload Resume link
  - Upload Job Description link
  - User profile dropdown
  - Logout button
- Main content area
- Footer (optional)

**Responsive Design**:
- Mobile: Single column, hamburger menu
- Tablet: Two columns where appropriate
- Desktop: Full layout

---

### 2. API Service Layer

**File**: `src/services/api.js`

**Features**:
- Axios instance with base URL
- JWT token management
- Request/response interceptors
- Error handling
- Token refresh logic

**Services**:

#### Authentication Service
```javascript
- login(email, password)
- register(email, password, fullName)
- logout()
- refreshToken()
- getToken()
- setToken(token)
```

#### Resume Service
```javascript
- uploadResume(file, title)
- listResumes()
- deleteResume(id)
- getResume(id)
```

#### Job Description Service
```javascript
- uploadJobDescription(content, title, company)
- listJobDescriptions()
- deleteJobDescription(id)
- getJobDescription(id)
```

#### Analysis Service
```javascript
- calculateScore(resumeId, jobId)
- getAnalysisResults(analysisId)
- listAnalysisResults()
```

---

### 3. Deployment Configuration

#### Frontend Deployment (Vercel)

**File**: `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "VITE_API_URL": "@vite_api_url"
  }
}
```

**Environment Variables**:
- `VITE_API_URL`: Backend API URL (e.g., https://api.example.com)

**Deployment Steps**:
1. Connect GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

---

#### Backend Deployment (Render/Railway)

**File**: `render.yaml` or `railway.json`

**Configuration**:
- Python 3.11 runtime
- Django application
- PostgreSQL database
- Environment variables

**Environment Variables**:
- `DEBUG`: False
- `ALLOWED_HOSTS`: Production domain
- `SECRET_KEY`: Production secret key
- `DATABASE_URL`: PostgreSQL connection string
- `CORS_ALLOWED_ORIGINS`: Frontend URL
- `JWT_SECRET`: JWT signing key

**Deployment Steps**:
1. Connect GitHub repository to Render/Railway
2. Set environment variables
3. Configure PostgreSQL database
4. Deploy automatically on push to main branch

---

#### Database Configuration (PostgreSQL)

**Setup**:
1. Create PostgreSQL database on Render/Railway
2. Configure connection pooling
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

**Backup**:
- Enable automated daily backups
- Retention period: 30 days

---

## User Flows

### Flow 1: New User Registration and Resume Upload

1. User visits application
2. Redirected to login page
3. Clicks "Register" link
4. Fills registration form
5. Submits registration
6. Auto-logged in
7. Redirected to dashboard
8. Clicks "Upload Resume"
9. Uploads resume file
10. Reviews parsed data
11. Confirms and saves
12. Returns to dashboard

### Flow 2: Resume Analysis

1. User on dashboard
2. Clicks "Upload Job Description"
3. Uploads job description
4. Returns to dashboard
5. Selects resume and job description
6. Clicks "Analyze"
7. System calculates ATS score
8. Redirected to results page
9. Views detailed analysis
10. Can download report or go back

### Flow 3: Resume Comparison

1. User on dashboard
2. Has multiple resumes and job descriptions
3. Selects different resume-job pairs
4. Compares ATS scores
5. Identifies best matches
6. Focuses on improving lowest-scoring resumes

---

## Technical Specifications

### Frontend

**Build Process**:
```bash
npm install
npm run dev      # Development
npm run build    # Production
npm run preview  # Preview production build
```

**Project Structure**:
```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── UploadResume.jsx
│   │   └── Results.jsx
│   ├── components/
│   │   ├── Layout.jsx
│   │   ├── Navigation.jsx
│   │   ├── ErrorBoundary.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ScoreDisplay.jsx
│   ├── services/
│   │   └── api.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useApi.js
│   ├── App.jsx
│   └── main.jsx
├── public/
├── vite.config.js
├── tailwind.config.js
├── package.json
└── vercel.json
```

**Dependencies**:
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.x.x",
  "axios": "^1.x.x",
  "react-hook-form": "^7.x.x",
  "tailwindcss": "^3.x.x"
}
```

### Backend

**No changes required** - All backend modules are frozen and production-ready.

---

## Success Criteria

✅ Users can register and login  
✅ Users can upload resumes  
✅ Users can upload job descriptions  
✅ Users can view ATS analysis results  
✅ Dashboard displays all user data  
✅ Results page shows detailed score breakdown  
✅ Frontend connects to backend APIs  
✅ Frontend deployed on Vercel  
✅ Backend deployed on Render/Railway  
✅ Database deployed on PostgreSQL  
✅ All pages are responsive  
✅ Error handling works correctly  
✅ Loading states display properly  

---

## Timeline

**Phase 1 (Frontend)**: 3-4 days
- React setup and configuration
- All pages implementation
- API service layer
- Testing

**Phase 2 (Deployment)**: 1-2 days
- Vercel configuration
- Render/Railway configuration
- PostgreSQL setup
- Environment configuration

**Total**: 4-6 days

---

## Notes

- All backend modules are production-ready and frozen
- No modifications to authentication, resume parsing, or ATS scoring
- Frontend uses modern React patterns and best practices
- Deployment uses industry-standard platforms
- Application is fully responsive
- Error handling is comprehensive
- User experience is intuitive and clean

