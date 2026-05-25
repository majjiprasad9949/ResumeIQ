# MVP Implementation Plan: ResumeIQ

## Overview

This is the streamlined MVP implementation plan focusing only on core features:
- React frontend with essential pages
- API connections to existing backend
- Deployment configuration

**FROZEN MODULES (Do NOT modify):**
- ✅ Authentication (users app)
- ✅ Resume upload & parsing (resumes app)
- ✅ ATS scoring engine (analysis app)
- ✅ Django backend infrastructure


---

## Phase 1: React Frontend Implementation

### 1.1 Set Up React Project

- [ ] 1.1 Initialize React project with Vite
  - Create React project with `npm create vite@latest`
  - Install dependencies: React Router, Axios, TailwindCSS, React Hook Form
  - Configure environment variables for API endpoints
  - Set up project structure (pages, components, services, hooks)
  - _Requirements: 15.1-15.9_

### 1.2 Implement Authentication Pages

- [ ] 1.2 Create Login page
  - Build login form with email and password fields
  - Implement form validation
  - Handle login errors
  - Store JWT token in localStorage
  - Redirect to dashboard on success
  - _Requirements: 15.1-15.9_

- [ ] 1.3 Create Register page
  - Build registration form with email, password, full name
  - Implement form validation
  - Handle registration errors
  - Auto-login after successful registration
  - _Requirements: 15.1-15.9_

### 1.3 Implement Resume Management Pages

- [ ] 1.4 Create Resume Upload page
  - Build drag-and-drop upload area
  - Display file name and size
  - Show upload progress
  - Handle upload errors
  - Display parsed resume data
  - _Requirements: 15.1-15.9_

- [ ] 1.5 Create Dashboard page
  - Display list of uploaded resumes
  - Display list of job descriptions
  - Show latest ATS scores
  - Implement delete functionality
  - Link to analysis results
  - _Requirements: 16.1-16.8_

### 1.4 Implement Analysis Pages

- [ ] 1.6 Create Results page
  - Display ATS score with visual indicator (gauge/progress bar)
  - Display score breakdown by component:
    - Keyword Match (30%)
    - Skills Match (25%)
    - Resume Structure (20%)
    - Experience Match (15%)
    - Grammar Quality (10%)
  - Display missing keywords (top 10)
  - Display skill gaps (top 10)
  - Display risk level indicator
  - _Requirements: 16.1-16.8_

### 1.5 Implement API Service Layer

- [ ] 1.7 Create API service module
  - Create axios instance with base URL and interceptors
  - Implement authentication service (login, register, logout)
  - Implement resume service (upload, list, delete)
  - Implement job description service (upload, list, delete)
  - Implement analysis service (calculate score, get results)
  - Handle JWT token refresh
  - _Requirements: 14.1-14.20_

### 1.6 Implement Navigation and Layout

- [ ] 1.8 Create main layout component
  - Build navigation bar with logo and user menu
  - Implement logout functionality
  - Add responsive design for mobile/tablet
  - _Requirements: 15.1-15.9_

- [ ] 1.9 Create routing configuration
  - Set up React Router with protected routes
  - Redirect unauthenticated users to login
  - Implement route guards
  - _Requirements: 15.1-15.9_

### 1.7 Implement Error Handling and Loading States

- [ ] 1.10 Create error boundary component
  - Display user-friendly error messages
  - Show error tracking ID
  - Provide retry options
  - _Requirements: 20.1-20.8_

- [ ] 1.11 Create loading indicators
  - Display loading state during API calls
  - Show progress indicators for uploads
  - _Requirements: 15.5_

### 1.8 Implement Responsive Design

- [ ] 1.12 Ensure responsive design
  - Test on various screen sizes (mobile, tablet, desktop)
  - Implement mobile-friendly navigation
  - Optimize touch interactions
  - _Requirements: 15.1-15.9_

---

## Phase 2: Frontend Testing

### 2.1 Component Tests

- [ ] 2.1 Write component tests
  - Test form validation
  - Test error handling
  - Test loading states
  - Test API integration
  - _Requirements: 15.1-16.8_

### 2.2 Integration Tests

- [ ] 2.2 Write integration tests
  - Test login → upload → analyze flow
  - Test error scenarios
  - Test navigation
  - _Requirements: 15.1-16.8_

---

## Phase 3: Deployment Configuration

### 3.1 Frontend Deployment (Vercel)

- [ ] 3.1 Configure Vercel deployment
  - Create vercel.json configuration
  - Set up environment variables for production
  - Configure build command and output directory
  - Set up automatic deployments from GitHub
  - _Requirements: 21.1-21.7_

### 3.2 Backend Deployment (Render/Railway)

- [ ] 3.2 Configure Render/Railway deployment
  - Create render.yaml or railway.json configuration
  - Set up environment variables for production
  - Configure database connection for production PostgreSQL
  - Set up automatic deployments from GitHub
  - Configure CORS for production frontend URL
  - _Requirements: 21.1-21.7_

### 3.3 Database Configuration

- [ ] 3.3 Set up production PostgreSQL
  - Create PostgreSQL database on Render/Railway
  - Configure connection pooling
  - Set up automated backups
  - Create database migrations
  - _Requirements: 21.6_

### 3.4 Environment Configuration

- [ ] 3.4 Create production environment files
  - Create .env.production for backend
  - Create .env.production for frontend
  - Document all required environment variables
  - _Requirements: 21.1-21.7_

### 3.5 Deployment Documentation

- [ ] 3.5 Create deployment guide
  - Document deployment procedures
  - Create runbooks for common issues
  - Document scaling procedures
  - _Requirements: 21.1-21.7_

---

## Task Dependencies

```
Phase 1 (Frontend)
├─ 1.1 React Setup
├─ 1.2 Login Page
├─ 1.3 Register Page
├─ 1.4 Resume Upload Page
├─ 1.5 Dashboard Page
├─ 1.6 Results Page
├─ 1.7 API Service Layer
├─ 1.8 Layout Component
├─ 1.9 Routing
├─ 1.10 Error Boundary
├─ 1.11 Loading Indicators
└─ 1.12 Responsive Design

Phase 2 (Testing)
├─ 2.1 Component Tests (depends on Phase 1)
└─ 2.2 Integration Tests (depends on Phase 1)

Phase 3 (Deployment)
├─ 3.1 Vercel Frontend (depends on Phase 1)
├─ 3.2 Render/Railway Backend (depends on Phase 1)
├─ 3.3 PostgreSQL Database (depends on Phase 1)
├─ 3.4 Environment Configuration (depends on Phase 1)
└─ 3.5 Deployment Documentation (depends on Phase 1)
```

---

## Parallel Execution Opportunities

**Can run in parallel:**
- Phase 1 tasks (all frontend components can be built independently)
- Phase 2 tasks (testing can start after Phase 1)
- Phase 3 tasks (deployment configuration can be done in parallel)

**Must run sequentially:**
- Phase 1 → Phase 2 (need frontend before testing)
- Phase 1 → Phase 3 (need frontend before deployment)

---

## API Endpoints to Connect

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh

### Resumes
- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes` - List resumes
- `DELETE /api/resumes/{id}` - Delete resume

### Job Descriptions
- `POST /api/job-descriptions/upload` - Upload job description
- `GET /api/job-descriptions` - List job descriptions
- `DELETE /api/job-descriptions/{id}` - Delete job description

### Analysis
- `POST /api/analysis/ats/calculate_score` - Calculate ATS score
- `GET /api/analysis/ats/{id}` - Get analysis results

---

## Frontend Pages Summary

### 1. Login Page
- Email and password input fields
- Submit button
- Link to register page
- Error message display

### 2. Register Page
- Email, password, full name input fields
- Submit button
- Link to login page
- Error message display

### 3. Resume Upload Page
- Drag-and-drop upload area
- File input button
- Upload progress indicator
- Parsed resume data display
- Back to dashboard button

### 4. Dashboard Page
- List of uploaded resumes with delete buttons
- List of job descriptions with delete buttons
- Latest ATS scores for each resume-job pair
- Links to view detailed results
- Upload new resume button
- Upload new job description button

### 5. Results Page
- ATS score display (0-100 with visual indicator)
- Score breakdown (5 components with percentages)
- Missing keywords list (top 10)
- Skill gaps list (top 10)
- Risk level indicator (low/moderate/high)
- Back to dashboard button

---

## Notes

- All backend modules are frozen and will NOT be modified
- Frontend uses TailwindCSS for styling
- All API calls use JWT authentication
- Error handling is consistent across all pages
- Responsive design works on mobile, tablet, and desktop
- Deployment uses industry-standard platforms (Vercel, Render/Railway, PostgreSQL)

