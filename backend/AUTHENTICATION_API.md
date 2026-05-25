# Authentication API Documentation

## Overview

The Authentication API provides endpoints for user registration, login, logout, password management, and email verification. All endpoints use JWT (JSON Web Token) for authentication.

## Base URL

```
http://localhost:8000/api/users/
```

## Authentication

### JWT Token

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Token Expiration

- **Access Token**: 24 hours
- **Refresh Token**: 7 days

## Endpoints

### 1. User Registration

**Endpoint**: `POST /api/users/register/`

**Permission**: Public (AllowAny)

**Description**: Register a new user account

**Request Body**:
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

**Response** (201 Created):
```json
{
  "message": "User registered successfully. Please verify your email.",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "email": ["Email already registered."],
  "password": ["Passwords do not match."]
}
```

**Validation Rules**:
- Email must be unique
- Email must be valid format
- Password must be at least 8 characters
- Password must contain uppercase, lowercase, and numbers
- Passwords must match

---

### 2. User Login

**Endpoint**: `POST /api/users/auth/login/`

**Permission**: Public (AllowAny)

**Description**: Login with email and password to get JWT tokens

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_email_verified": true
  }
}
```

**Error Response** (401 Unauthorized):
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 3. Refresh Token

**Endpoint**: `POST /api/users/auth/refresh/`

**Permission**: Public (AllowAny)

**Description**: Get a new access token using refresh token

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Response** (401 Unauthorized):
```json
{
  "detail": "Token is invalid or expired"
}
```

---

### 4. User Logout

**Endpoint**: `POST /api/users/logout/`

**Permission**: Authenticated (IsAuthenticated)

**Description**: Logout user and blacklist refresh token

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "message": "Logged out successfully."
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Token is invalid or expired"
}
```

---

### 5. Get Current User

**Endpoint**: `GET /api/users/me/`

**Permission**: Authenticated (IsAuthenticated)

**Description**: Get current authenticated user details

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "location": "New York, USA",
  "bio": "Software Developer",
  "profile_picture": "https://example.com/profile.jpg",
  "email_notifications": true,
  "data_processing_consent": true,
  "is_email_verified": true,
  "email_verified_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "profile": {
    "current_job_title": "Senior Developer",
    "current_company": "Tech Corp",
    "years_of_experience": 5,
    "industry": "Technology",
    "target_job_title": "Tech Lead",
    "target_industry": "Technology",
    "total_resumes": 3,
    "total_optimizations": 5,
    "average_ats_score": 78.5,
    "created_at": "2024-01-10T08:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### 6. Update User Profile

**Endpoint**: `PUT/PATCH /api/users/update_profile/`

**Permission**: Authenticated (IsAuthenticated)

**Description**: Update current user profile information

**Request Body** (all fields optional):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "location": "New York, USA",
  "bio": "Software Developer",
  "profile_picture": "<file>",
  "email_notifications": true,
  "data_processing_consent": true
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "location": "New York, USA",
  "bio": "Software Developer",
  "profile_picture": "https://example.com/profile.jpg",
  "email_notifications": true,
  "data_processing_consent": true,
  "is_email_verified": true,
  "email_verified_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "profile": { ... }
}
```

---

### 7. Change Password

**Endpoint**: `POST /api/users/change_password/`

**Permission**: Authenticated (IsAuthenticated)

**Description**: Change user password

**Request Body**:
```json
{
  "old_password": "OldPassword123!",
  "new_password": "NewPassword456!",
  "new_password_confirm": "NewPassword456!"
}
```

**Response** (200 OK):
```json
{
  "message": "Password changed successfully."
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Old password is incorrect."
}
```

---

### 8. Forgot Password

**Endpoint**: `POST /api/users/forgot_password/`

**Permission**: Public (AllowAny)

**Description**: Request password reset link

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200 OK):
```json
{
  "message": "Password reset link sent to your email."
}
```

**Email Content**:
```
Hello John,

Please reset your password by clicking the link below:
http://localhost:3000/reset-password?token=<token>

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
ResumeIQ Team
```

**Error Response** (400 Bad Request):
```json
{
  "email": ["Email not found."]
}
```

---

### 9. Reset Password

**Endpoint**: `POST /api/users/reset_password/`

**Permission**: Public (AllowAny)

**Description**: Reset password with token

**Request Body**:
```json
{
  "token": "reset_token_from_email",
  "new_password": "NewPassword456!",
  "new_password_confirm": "NewPassword456!"
}
```

**Response** (200 OK):
```json
{
  "message": "Password reset successfully. You can now login with your new password."
}
```

**Error Response** (400 Bad Request):
```json
{
  "token": ["Token is invalid or expired."]
}
```

**Token Validity**: 1 hour

---

### 10. Verify Email

**Endpoint**: `POST /api/users/verify_email/`

**Permission**: Public (AllowAny)

**Description**: Verify email with token

**Request Body**:
```json
{
  "token": "verification_token_from_email"
}
```

**Response** (200 OK):
```json
{
  "message": "Email verified successfully."
}
```

**Error Response** (400 Bad Request):
```json
{
  "token": ["Token is invalid or expired."]
}
```

**Token Validity**: 24 hours

---

### 11. Resend Verification Email

**Endpoint**: `POST /api/users/resend_verification_email/`

**Permission**: Public (AllowAny)

**Description**: Resend email verification link

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200 OK):
```json
{
  "message": "Verification email sent to your email address."
}
```

**Error Response** (400 Bad Request):
```json
{
  "message": "Email is already verified."
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Authentication Flow

### Registration Flow
```
1. User submits registration form
2. System validates input
3. User account created
4. Email verification token generated
5. Verification email sent
6. JWT tokens returned
7. User redirected to verify email page
```

### Login Flow
```
1. User submits login credentials
2. System validates credentials
3. Last login timestamp updated
4. JWT tokens generated
5. Tokens returned to client
6. Client stores tokens in localStorage
```

### Password Reset Flow
```
1. User requests password reset
2. System generates reset token
3. Reset email sent with token
4. User clicks link in email
5. User submits new password
6. System validates token and password
7. Password updated
8. Token marked as used
9. User can login with new password
```

### Email Verification Flow
```
1. User registers account
2. System generates verification token
3. Verification email sent with token
4. User clicks link in email
5. System validates token
6. Email marked as verified
7. Token marked as used
8. User can access all features
```

---

## Security Considerations

### Password Security
- Minimum 8 characters
- Must contain uppercase letters
- Must contain lowercase letters
- Must contain numbers
- Hashed with bcrypt

### Token Security
- JWT tokens signed with SECRET_KEY
- Access tokens expire after 24 hours
- Refresh tokens expire after 7 days
- Tokens can be blacklisted on logout
- Tokens include user ID and email

### Email Security
- Verification tokens expire after 24 hours
- Password reset tokens expire after 1 hour
- Tokens are one-time use
- Tokens are cryptographically secure

### Rate Limiting
- Implement rate limiting on authentication endpoints
- Prevent brute force attacks
- Limit password reset requests

---

## Usage Examples

### JavaScript/Fetch

```javascript
// Registration
const registerResponse = await fetch('http://localhost:8000/api/users/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    first_name: 'John',
    last_name: 'Doe',
    password: 'SecurePassword123!',
    password_confirm: 'SecurePassword123!'
  })
});

// Login
const loginResponse = await fetch('http://localhost:8000/api/users/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePassword123!'
  })
});

const { access, refresh } = await loginResponse.json();

// Get current user
const userResponse = await fetch('http://localhost:8000/api/users/me/', {
  headers: { 'Authorization': `Bearer ${access}` }
});

// Refresh token
const refreshResponse = await fetch('http://localhost:8000/api/users/auth/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ refresh })
});

// Logout
const logoutResponse = await fetch('http://localhost:8000/api/users/logout/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access}`
  },
  body: JSON.stringify({ refresh })
});
```

### Python/Requests

```python
import requests

# Registration
response = requests.post(
    'http://localhost:8000/api/users/register/',
    json={
        'email': 'user@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'SecurePassword123!',
        'password_confirm': 'SecurePassword123!'
    }
)

# Login
response = requests.post(
    'http://localhost:8000/api/users/auth/login/',
    json={
        'email': 'user@example.com',
        'password': 'SecurePassword123!'
    }
)

tokens = response.json()
access_token = tokens['access']

# Get current user
response = requests.get(
    'http://localhost:8000/api/users/me/',
    headers={'Authorization': f'Bearer {access_token}'}
)

# Refresh token
response = requests.post(
    'http://localhost:8000/api/users/auth/refresh/',
    json={'refresh': tokens['refresh']}
)

# Logout
response = requests.post(
    'http://localhost:8000/api/users/logout/',
    headers={'Authorization': f'Bearer {access_token}'},
    json={'refresh': tokens['refresh']}
)
```

---

## Testing

### Test Cases

1. **Registration**
   - Valid registration
   - Duplicate email
   - Invalid email format
   - Weak password
   - Mismatched passwords

2. **Login**
   - Valid credentials
   - Invalid email
   - Invalid password
   - Non-existent user

3. **Token Refresh**
   - Valid refresh token
   - Expired refresh token
   - Invalid refresh token

4. **Password Management**
   - Change password with correct old password
   - Change password with incorrect old password
   - Forgot password
   - Reset password with valid token
   - Reset password with expired token

5. **Email Verification**
   - Verify email with valid token
   - Verify email with expired token
   - Resend verification email

---

## Troubleshooting

### Common Issues

**"Email already registered"**
- The email is already associated with an account
- Use forgot password to reset if you forgot your password
- Use a different email address

**"Passwords do not match"**
- Ensure password and password_confirm are identical
- Check for extra spaces or special characters

**"Token is invalid or expired"**
- Token has expired (1 hour for password reset, 24 hours for email verification)
- Request a new token

**"No active account found with the given credentials"**
- Email or password is incorrect
- Check email spelling
- Verify caps lock is off

**"Email not verified"**
- Check your email for verification link
- Click the verification link
- Use resend verification email if link expired

---

## Support

For issues or questions, please contact support or open an issue on GitHub.
