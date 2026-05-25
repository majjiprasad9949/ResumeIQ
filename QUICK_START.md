# Quick Start Guide - Authentication Module

## Installation (5 minutes)

### 1. Setup Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Server running at: `http://localhost:8000`

---

## Testing Authentication (10 minutes)

### Register User
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

Save the `access` token from response.

### Get Current User
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

### Update Profile
```bash
curl -X PATCH http://localhost:8000/api/users/update_profile/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "phone_number": "+1234567890",
    "location": "New York, USA"
  }'
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/auth/login/` | Login user |
| POST | `/api/users/auth/refresh/` | Refresh token |
| POST | `/api/users/logout/` | Logout user |

### User Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me/` | Get current user |
| PUT | `/api/users/update_profile/` | Update profile |
| PATCH | `/api/users/update_profile/` | Partial update |

### Password Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/change_password/` | Change password |
| POST | `/api/users/forgot_password/` | Request reset |
| POST | `/api/users/reset_password/` | Reset password |

### Email Verification
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/verify_email/` | Verify email |
| POST | `/api/users/resend_verification_email/` | Resend verification |

---

## Admin Panel

Access at: `http://localhost:8000/admin/`

**Manage:**
- Users
- User Profiles
- Password Reset Tokens
- Email Verification Tokens

---

## Environment Variables

```bash
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend
FRONTEND_URL=http://localhost:3000

# Database
DB_NAME=ai_resume_optimizer
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@airesume.com
```

---

## Common Tasks

### Create Test User
```bash
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user(
    email='test@example.com',
    password='TestPassword123!',
    first_name='Test',
    last_name='User'
)
```

### Reset Database
```bash
python manage.py migrate zero
python manage.py migrate
```

### Run Tests
```bash
python manage.py test
```

### Check Migrations
```bash
python manage.py showmigrations
```

---

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
psql -U postgres -d ai_resume_optimizer
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Email Not Sending
- Check EMAIL_BACKEND in .env
- For development, use console backend
- Check email credentials

### Token Expired
- Use refresh endpoint to get new access token
- Access token expires after 24 hours
- Refresh token expires after 7 days

---

## Documentation

- **Full API Docs**: `AUTHENTICATION_API.md`
- **Testing Guide**: `AUTHENTICATION_TESTING.md`
- **Implementation Details**: `AUTHENTICATION_IMPLEMENTATION.md`
- **Backend Structure**: `BACKEND_STRUCTURE.md`

---

## Next Steps

1. ✅ Authentication module complete
2. ⏳ Resume management module
3. ⏳ Job management module
4. ⏳ Analysis & NLP module
5. ⏳ Frontend integration
6. ⏳ Testing & deployment

---

## Support

For issues or questions:
1. Check documentation files
2. Review error messages
3. Check Django logs
4. Open GitHub issue

---

**Status**: Authentication Module Complete ✅
**Ready for**: Frontend Integration
