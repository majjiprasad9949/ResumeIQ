# Quick Reference Card

## Backend API Endpoints

### Authentication
```
POST   /api/auth/register          - Register new user
POST   /api/auth/login             - Login user
POST   /api/auth/refresh           - Refresh JWT token
POST   /api/auth/password-reset    - Reset password
GET    /api/users/profile          - Get user profile
PUT    /api/users/profile          - Update user profile
```

### Resumes
```
POST   /api/resumes/upload         - Upload resume
GET    /api/resumes                - List resumes
GET    /api/resumes/{id}           - Get resume details
DELETE /api/resumes/{id}           - Delete resume
GET    /api/resumes/{id}/versions  - Get version history
POST   /api/resumes/{id}/revert    - Revert to version
```

### Job Descriptions
```
POST   /api/job-descriptions/upload - Upload job description
GET    /api/job-descriptions        - List job descriptions
GET    /api/job-descriptions/{id}   - Get job details
DELETE /api/job-descriptions/{id}   - Delete job description
```

### Analysis
```
POST   /api/analysis/ats/calculate_score - Calculate ATS score
GET    /api/analysis/ats/{id}            - Get analysis results
GET    /api/analysis/ats                 - List analysis results
```

---

## Frontend Pages

| Page | URL | Purpose |
|------|-----|---------|
| Login | `/login` | User authentication |
| Register | `/register` | New user registration |
| Dashboard | `/dashboard` | Main hub |
| Upload Resume | `/upload-resume` | Upload and parse resume |
| Results | `/results/{resumeId}/{jobId}` | View ATS analysis |

---

## Environment Variables

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
JWT_SECRET=your-jwt-secret
```

---

## ATS Scoring Breakdown

| Component | Weight | Score Range |
|-----------|--------|-------------|
| Keyword Match | 30% | 0-100 |
| Skills Match | 25% | 0-100 |
| Resume Structure | 20% | 0-100 |
| Experience Match | 15% | 0-100 |
| Grammar Quality | 10% | 0-100 |
| **Total** | **100%** | **0-100** |

### Risk Levels
- **Low Risk**: Score >= 75
- **Moderate Risk**: Score 60-74
- **High Risk**: Score < 60

---

## Frontend Setup Commands

```bash
# Create project
npm create vite@latest frontend -- --template react

# Install dependencies
npm install
npm install react-router-dom axios react-hook-form tailwindcss

# Configure Tailwind
npx tailwindcss init -p

# Development
npm run dev

# Build
npm run build

# Preview
npm run preview
```

---

## Backend Setup Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test
```

---

## Deployment Commands

### Frontend (Vercel)
```bash
# Push to GitHub
git add .
git commit -m "Deploy frontend"
git push origin main

# Vercel automatically deploys
```

### Backend (Render/Railway)
```bash
# Push to GitHub
git add .
git commit -m "Deploy backend"
git push origin main

# Render/Railway automatically deploys
```

---

## Common API Calls

### Register
```javascript
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

### Login
```javascript
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Upload Resume
```javascript
POST /api/resumes/upload
Content-Type: multipart/form-data
{
  "file": <file>,
  "title": "My Resume"
}
```

### Calculate ATS Score
```javascript
POST /api/analysis/ats/calculate_score
{
  "resume_id": "uuid",
  "job_id": "uuid"
}
```

---

## File Structure

### Frontend
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
│   ├── services/
│   │   └── api.js
│   ├── hooks/
│   ├── App.jsx
│   └── main.jsx
├── vite.config.js
├── tailwind.config.js
└── package.json
```

### Backend
```
backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   ├── resumes/
│   ├── jobs/
│   └── analysis/
├── manage.py
└── requirements.txt
```

---

## Debugging Tips

### Frontend
1. Open DevTools (F12)
2. Check Network tab for API calls
3. Check Console for errors
4. Check Local Storage for tokens

### Backend
1. Check Django logs
2. Check database connection
3. Check environment variables
4. Run `python manage.py test`

---

## Frozen Modules (Do NOT modify)

- ✅ Authentication (users app)
- ✅ Resume Management (resumes app)
- ✅ ATS Scoring (analysis app)
- ✅ Backend Infrastructure (config)

---

## Removed Features (Do NOT implement)

- ❌ AI Chatbot
- ❌ Cover Letter Generator
- ❌ Interview Question Generator
- ❌ sentence-transformers
- ❌ Redis Caching
- ❌ Docker
- ❌ Analytics
- ❌ LinkedIn Analysis

---

## Key Dates

- **Backend**: ✅ Complete
- **Frontend**: In Progress (3-4 days)
- **Deployment**: Ready (1-2 days)
- **MVP Launch**: 4-6 days

---

## Important Links

- [MVP Specification](./MVP_SPECIFICATION.md)
- [MVP Tasks](./MVP_TASKS.md)
- [Frozen Modules](./FROZEN_MODULES.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Frontend Quickstart](./FRONTEND_QUICKSTART.md)

---

## Support

For issues:
1. Check the relevant documentation
2. Review error messages
3. Check logs
4. Verify environment variables
5. Test API endpoints manually

---

## Success Checklist

- [ ] Frontend pages created
- [ ] API integration working
- [ ] All tests passing
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Render/Railway
- [ ] Database configured
- [ ] Environment variables set
- [ ] CORS configured
- [ ] JWT tokens working
- [ ] Resume upload working
- [ ] ATS scoring working
- [ ] Results page displaying
- [ ] Error handling working
- [ ] Loading states working
- [ ] Responsive design working

---

**Ready to build! 🚀**

