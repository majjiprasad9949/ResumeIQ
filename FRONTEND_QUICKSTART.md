# Frontend Quick Start Guide

This guide helps you get started with React frontend development for the  ResumeIQ MVP.

---

## Prerequisites

- Node.js 16+ and npm
- Git
- Code editor (VS Code recommended)
- Backend API running locally or deployed

---

## Project Setup

### Step 1: Create React Project

```bash
# Create new Vite React project
npm create vite@latest frontend -- --template react

# Navigate to project
cd frontend

# Install dependencies
npm install
```

### Step 2: Install Additional Dependencies

```bash
npm install react-router-dom axios react-hook-form tailwindcss postcss autoprefixer
npm install -D tailwindcss postcss autoprefixer
```

### Step 3: Configure Tailwind CSS

```bash
# Initialize Tailwind
npx tailwindcss init -p
```

Update `tailwind.config.js`:
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Update `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Step 4: Create Project Structure

```bash
mkdir -p src/{pages,components,services,hooks,utils}
```

---

## Project Structure

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
│   ├── utils/
│   │   └── constants.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── vite.config.js
├── tailwind.config.js
├── package.json
└── .env.local
```

---

## Environment Configuration

Create `.env.local`:
```
VITE_API_URL=http://localhost:8000
```

For production, create `.env.production`:
```
VITE_API_URL=https://your-backend-url.com
```

---

## API Service Layer

Create `src/services/api.js`:

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/api/auth/refresh`, {
          refresh: refreshToken,
        });

        localStorage.setItem('access_token', response.data.access);
        api.defaults.headers.Authorization = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication Service
export const authService = {
  register: (email, password, fullName) =>
    api.post('/auth/register', { email, password, full_name: fullName }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  
  getProfile: () => api.get('/users/profile'),
  
  updateProfile: (data) => api.put('/users/profile', data),
};

// Resume Service
export const resumeService = {
  upload: (file, title) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    return api.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  list: () => api.get('/resumes'),
  
  get: (id) => api.get(`/resumes/${id}`),
  
  delete: (id) => api.delete(`/resumes/${id}`),
  
  getVersions: (id) => api.get(`/resumes/${id}/versions`),
  
  revert: (id, versionId) =>
    api.post(`/resumes/${id}/revert`, { version_id: versionId }),
};

// Job Description Service
export const jobService = {
  upload: (content, title, company) =>
    api.post('/job-descriptions/upload', { content, title, company }),
  
  list: () => api.get('/job-descriptions'),
  
  get: (id) => api.get(`/job-descriptions/${id}`),
  
  delete: (id) => api.delete(`/job-descriptions/${id}`),
};

// Analysis Service
export const analysisService = {
  calculateScore: (resumeId, jobId) =>
    api.post('/analysis/ats/calculate_score', {
      resume_id: resumeId,
      job_id: jobId,
    }),
  
  getResults: (analysisId) => api.get(`/analysis/ats/${analysisId}`),
  
  listResults: () => api.get('/analysis/ats'),
};

export default api;
```

---

## Custom Hooks

Create `src/hooks/useAuth.js`:

```javascript
import { useState, useEffect } from 'react';
import { authService } from '../services/api';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await authService.getProfile();
      setUser(response.data);
    } catch (err) {
      setError(err.message);
      localStorage.removeItem('access_token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await authService.login(email, password);
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      await fetchUser();
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, password, fullName) => {
    setLoading(true);
    try {
      const response = await authService.register(email, password, fullName);
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      await fetchUser();
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return { user, loading, error, login, register, logout, isAuthenticated: !!user };
};
```

Create `src/hooks/useApi.js`:

```javascript
import { useState, useCallback } from 'react';

export const useApi = (apiFunction) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiFunction(...args);
        setData(response.data);
        return response.data;
      } catch (err) {
        const errorMessage = err.response?.data?.detail || err.message;
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  return { data, loading, error, execute };
};
```

---

## Core Components

Create `src/components/Layout.jsx`:

```javascript
import { Outlet } from 'react-router-dom';
import Navigation from './Navigation';

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
```

Create `src/components/Navigation.jsx`:

```javascript
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Navigation() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">
          Resume Optimizer
        </Link>
        
        <div className="flex gap-4">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="text-gray-600 hover:text-gray-900">
                Dashboard
              </Link>
              <span className="text-gray-600">{user?.email}</span>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-gray-600 hover:text-gray-900">
                Login
              </Link>
              <Link to="/register" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
```

Create `src/components/LoadingSpinner.jsx`:

```javascript
export default function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center py-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}
```

Create `src/components/ScoreDisplay.jsx`:

```javascript
export default function ScoreDisplay({ score, riskLevel }) {
  const getRiskColor = (level) => {
    switch (level) {
      case 'low':
        return 'text-green-600';
      case 'moderate':
        return 'text-yellow-600';
      case 'high':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-8 text-center">
      <div className="text-6xl font-bold text-blue-600 mb-4">{score}</div>
      <div className="text-xl text-gray-600 mb-4">ATS Score</div>
      <div className={`text-lg font-semibold ${getRiskColor(riskLevel)}`}>
        {riskLevel?.toUpperCase()} RISK
      </div>
    </div>
  );
}
```

---

## Page Templates

Create `src/pages/Login.jsx`:

```javascript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <div className="bg-white rounded-lg shadow p-8">
        <h1 className="text-2xl font-bold mb-6">Login</h1>
        
        {error && <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border rounded px-3 py-2"
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border rounded px-3 py-2"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <p className="mt-4 text-center">
          Don't have an account? <Link to="/register" className="text-blue-600 hover:underline">Register</Link>
        </p>
      </div>
    </div>
  );
}
```

---

## Running the Development Server

```bash
# Start development server
npm run dev

# Server runs at http://localhost:5173
```

---

## Building for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Common Tasks

### Add a New Page

1. Create file in `src/pages/`
2. Add route in `App.jsx`
3. Add navigation link in `Navigation.jsx`

### Add a New Component

1. Create file in `src/components/`
2. Import and use in pages

### Make API Call

```javascript
import { resumeService } from '../services/api';
import { useApi } from '../hooks/useApi';

const { data, loading, error, execute } = useApi(resumeService.list);

// Call API
await execute();
```

---

## Debugging

### Check API Calls

1. Open browser DevTools (F12)
2. Go to Network tab
3. Make API call
4. Check request/response

### Check Console Errors

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for error messages

### Check Local Storage

1. Open browser DevTools (F12)
2. Go to Application tab
3. Check Local Storage for tokens

---

## Next Steps

1. Implement all pages (Login, Register, Dashboard, Upload, Results)
2. Test API integration
3. Add error handling
4. Add loading states
5. Test responsive design
6. Deploy to Vercel

---

## Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [React Router Documentation](https://reactrouter.com)
- [Axios Documentation](https://axios-http.com)

