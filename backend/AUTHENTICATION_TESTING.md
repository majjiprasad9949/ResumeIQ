# Authentication Module Testing Guide

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL running
- Django project configured
- Virtual environment activated

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## Testing with cURL

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!"
  }'
```

**Expected Response** (201 Created):
```json
{
  "message": "User registered successfully. Please verify your email.",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. User Login

```bash
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPassword123!"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "is_email_verified": false
  }
}
```

### 3. Get Current User

```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer <access_token>"
```

### 4. Update Profile

```bash
curl -X PATCH http://localhost:8000/api/users/update_profile/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "phone_number": "+1234567890",
    "location": "New York, USA",
    "bio": "Software Developer"
  }'
```

### 5. Change Password

```bash
curl -X POST http://localhost:8000/api/users/change_password/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "old_password": "TestPassword123!",
    "new_password": "NewPassword456!",
    "new_password_confirm": "NewPassword456!"
  }'
```

### 6. Forgot Password

```bash
curl -X POST http://localhost:8000/api/users/forgot_password/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com"
  }'
```

### 7. Reset Password

```bash
curl -X POST http://localhost:8000/api/users/reset_password/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "<reset_token_from_email>",
    "new_password": "NewPassword456!",
    "new_password_confirm": "NewPassword456!"
  }'
```

### 8. Verify Email

```bash
curl -X POST http://localhost:8000/api/users/verify_email/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "<verification_token_from_email>"
  }'
```

### 9. Resend Verification Email

```bash
curl -X POST http://localhost:8000/api/users/resend_verification_email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com"
  }'
```

### 10. Refresh Token

```bash
curl -X POST http://localhost:8000/api/users/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

### 11. Logout

```bash
curl -X POST http://localhost:8000/api/users/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

## Testing with Postman

### Setup

1. **Create Environment Variables**
   - `base_url`: http://localhost:8000
   - `access_token`: (will be set after login)
   - `refresh_token`: (will be set after login)

2. **Create Collection**: ResumeIQ

### Test Cases

#### 1. Register User
- **Method**: POST
- **URL**: `{{base_url}}/api/users/register/`
- **Body** (JSON):
```json
{
  "email": "testuser@example.com",
  "first_name": "Test",
  "last_name": "User",
  "password": "TestPassword123!",
  "password_confirm": "TestPassword123!"
}
```
- **Tests**:
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response has tokens", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.tokens).to.have.property('access');
    pm.expect(jsonData.tokens).to.have.property('refresh');
});

pm.environment.set("access_token", pm.response.json().tokens.access);
pm.environment.set("refresh_token", pm.response.json().tokens.refresh);
```

#### 2. Login User
- **Method**: POST
- **URL**: `{{base_url}}/api/users/auth/login/`
- **Body** (JSON):
```json
{
  "email": "testuser@example.com",
  "password": "TestPassword123!"
}
```
- **Tests**:
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has tokens", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access');
    pm.expect(jsonData).to.have.property('refresh');
});

pm.environment.set("access_token", pm.response.json().access);
pm.environment.set("refresh_token", pm.response.json().refresh);
```

#### 3. Get Current User
- **Method**: GET
- **URL**: `{{base_url}}/api/users/me/`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Tests**:
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has user data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('email');
    pm.expect(jsonData).to.have.property('first_name');
});
```

#### 4. Update Profile
- **Method**: PATCH
- **URL**: `{{base_url}}/api/users/update_profile/`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Body** (JSON):
```json
{
  "phone_number": "+1234567890",
  "location": "New York, USA",
  "bio": "Software Developer"
}
```
- **Tests**:
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Profile updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.phone_number).to.equal("+1234567890");
    pm.expect(jsonData.location).to.equal("New York, USA");
});
```

#### 5. Change Password
- **Method**: POST
- **URL**: `{{base_url}}/api/users/change_password/`
- **Headers**: `Authorization: Bearer {{access_token}}`
- **Body** (JSON):
```json
{
  "old_password": "TestPassword123!",
  "new_password": "NewPassword456!",
  "new_password_confirm": "NewPassword456!"
}
```
- **Tests**:
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Password changed message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.message).to.include("successfully");
});
```

## Testing with Python

### Unit Tests

Create `tests/test_authentication.py`:

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """Test user registration."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/users/register/'
    
    def test_valid_registration(self):
        """Test valid user registration."""
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
    
    def test_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123!'
        )
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_mismatched_passwords(self):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123!',
            'password_confirm': 'DifferentPassword456!'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(TestCase):
    """Test user login."""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/users/auth/login/'
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123!'
        )
    
    def test_valid_login(self):
        """Test valid login."""
        data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_invalid_password(self):
        """Test login with invalid password."""
        data = {
            'email': 'testuser@example.com',
            'password': 'WrongPassword123!'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTestCase(TestCase):
    """Test user profile operations."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123!'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_current_user(self):
        """Test getting current user."""
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')
    
    def test_update_profile(self):
        """Test updating user profile."""
        data = {
            'phone_number': '+1234567890',
            'location': 'New York, USA'
        }
        response = self.client.patch('/api/users/update_profile/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '+1234567890')
```

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test tests.test_authentication.UserRegistrationTestCase

# Run specific test method
python manage.py test tests.test_authentication.UserRegistrationTestCase.test_valid_registration

# Run with verbose output
python manage.py test -v 2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Manual Testing Checklist

### Registration
- [ ] Valid registration with all fields
- [ ] Registration with duplicate email
- [ ] Registration with invalid email format
- [ ] Registration with weak password
- [ ] Registration with mismatched passwords
- [ ] Verification email sent
- [ ] User profile created automatically

### Login
- [ ] Login with correct credentials
- [ ] Login with incorrect password
- [ ] Login with non-existent email
- [ ] Last login timestamp updated
- [ ] JWT tokens returned

### Token Management
- [ ] Access token works for authenticated endpoints
- [ ] Refresh token generates new access token
- [ ] Expired token rejected
- [ ] Invalid token rejected

### Profile Management
- [ ] Get current user details
- [ ] Update user information
- [ ] Update profile picture
- [ ] Update preferences

### Password Management
- [ ] Change password with correct old password
- [ ] Change password with incorrect old password
- [ ] Forgot password sends email
- [ ] Reset password with valid token
- [ ] Reset password with expired token
- [ ] Login with new password works

### Email Verification
- [ ] Verify email with valid token
- [ ] Verify email with expired token
- [ ] Resend verification email
- [ ] Email already verified message

### Logout
- [ ] Logout invalidates refresh token
- [ ] Cannot use refresh token after logout
- [ ] Access token still valid until expiration

## Performance Testing

### Load Testing with Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class AuthenticationUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def register(self):
        self.client.post("/api/users/register/", json={
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123!",
            "password_confirm": "TestPassword123!"
        })
    
    @task
    def login(self):
        self.client.post("/api/users/auth/login/", json={
            "email": "testuser@example.com",
            "password": "TestPassword123!"
        })
```

Run:
```bash
locust -f locustfile.py --host=http://localhost:8000
```

## Debugging

### Enable Debug Logging

Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Django Shell

```bash
python manage.py shell

# Check user
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(email='testuser@example.com')
print(user.is_email_verified)

# Check tokens
from apps.users.models import EmailVerificationToken
token = EmailVerificationToken.objects.filter(user=user).first()
print(token.is_valid())
```

## Troubleshooting

### Email Not Sending
- Check EMAIL_BACKEND in settings
- For development, use console backend
- Check email configuration

### Token Issues
- Verify SECRET_KEY is set
- Check token expiration times
- Verify JWT settings in settings.py

### Database Issues
- Run migrations: `python manage.py migrate`
- Check database connection
- Verify PostgreSQL is running

---

## Next Steps

1. Implement rate limiting on authentication endpoints
2. Add two-factor authentication
3. Add OAuth2 integration (Google, LinkedIn)
4. Add email confirmation for email changes
5. Add login history tracking
6. Add device management
7. Add security questions for password recovery

---

## Support

For issues or questions, please contact support or open an issue on GitHub.
