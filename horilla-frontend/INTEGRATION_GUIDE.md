# Horilla Frontend & Django Backend Integration Guide

This guide covers the complete integration between the Nuxt 4 frontend and Django REST API backend.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Configuration](#frontend-configuration)
4. [Authentication Flow](#authentication-flow)
5. [CORS Configuration](#cors-configuration)
6. [API Endpoints](#api-endpoints)
7. [Testing the Integration](#testing-the-integration)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Backend Requirements

- Django 4.2.23+
- Django REST Framework (DRF)
- SimpleJWT for token authentication
- django-cors-headers for CORS support
- PostgreSQL or SQLite database

### Frontend Requirements

- Node.js 18+
- npm/yarn/pnpm
- Nuxt 4

## Backend Setup

### 1. Ensure Django is Running

```bash
cd /path/to/horilla-talent
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

The Django backend should be accessible at `http://localhost:8000`

### 2. Verify CORS Configuration

Check `horilla/settings.py` for CORS middleware:

```python
# Should be in INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

# Should be in MIDDLEWARE
MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
]

# Allow credentials in CORS requests
CORS_ALLOW_CREDENTIALS = True
```

### 3. Verify JWT Authentication

Check for SimpleJWT configuration:

```python
# In settings.py
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

### 4. Verify API Endpoints

Ensure the API URL configuration in `horilla/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('api/', include('horilla_api.urls')),
    ...
]
```

Check that `horilla_api/urls.py` contains routes for all modules.

## Frontend Configuration

### 1. Environment Setup

Create `.env.local` in the frontend directory:

```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000

# Development
NODE_ENV=development
NUXT_PORT=3000

# Feature Flags
NUXT_PUBLIC_ENABLE_FACE_DETECTION=true
NUXT_PUBLIC_ENABLE_GEOFENCING=true
```

### 2. Update API Base URL

If your Django backend runs on a different host, update in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      apiTimeout: 30000,
    },
  },
})
```

### 3. Install Dependencies

```bash
cd horilla-frontend
npm install
```

### 4. Start Frontend Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Authentication Flow

### Request Sequence

1. **User Login**
   ```
   Frontend → POST /api/auth/login/ ← Backend
   Payload: { username, password }
   Response: { access, refresh, employee }
   ```

2. **Token Storage**
   - Access token stored in localStorage (client-side)
   - Tokens also set as secure cookies
   - Employee data stored in Pinia store and localStorage

3. **Authenticated Requests**
   ```
   Frontend → GET /api/employee/employees/
   Header: Authorization: Bearer <access_token>
   ← Backend
   ```

4. **Token Refresh** (automatic)
   ```
   Frontend → POST /api/auth/token/refresh/
   Payload: { refresh: <refresh_token> }
   Response: { access: <new_token> }
   ← Backend
   ```

### API Client Implementation

The API client (`utils/api-client.ts`) handles:

- Request interceptor: Adds Authorization header with access token
- Response interceptor: Handles 401 errors by refreshing token
- Automatic retry: Retries failed requests after token refresh
- Error handling: Converts errors to user-friendly messages

## CORS Configuration

### Development Setup

For local development with frontend on port 3000 and backend on port 8000:

**Backend (Django)**:
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Production Setup

For production deployment:

```python
# settings.py
import os

CORS_ALLOWED_ORIGINS = [
    "https://hr.yourdomain.com",
    "https://app.yourdomain.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://hr.yourdomain.com",
    "https://app.yourdomain.com",
]

ALLOWED_HOSTS = [
    "api.yourdomain.com",
    "yourdomain.com",
]

# Only allow HTTPS in production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## API Endpoints

### Authentication

#### Login
```
POST /api/auth/login/
Content-Type: application/json

{
  "username": "employee_username",
  "password": "employee_password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "employee": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "profile_image": "https://example.com/image.jpg",
    "company": 1
  },
  "face_detection": false,
  "geo_fencing": false
}
```

#### Refresh Token
```
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Employee Endpoints

#### List Employees
```
GET /api/employee/list/employees/?page=1&limit=10
Authorization: Bearer <access_token>

Response:
{
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "profile_image": "...",
      "date_of_birth": "1990-01-01",
      "gender": "M",
      "address": "...",
      "city": "...",
      "state": "...",
      "country": "...",
      "zip_code": "..."
    }
  ],
  "count": 500
}
```

#### Get Employee Details
```
GET /api/employee/employees/{id}/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "profile_image": "...",
  "company": 1
}
```

#### Get Work Information
```
GET /api/employee/employee-work-information/{employee_id}/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "employee_id": 1,
  "department": "IT",
  "job_position": "Software Engineer",
  "reporting_manager": "Jane Smith",
  "shift": "Morning",
  "work_type": "Full-time",
  "company": 1
}
```

### Attendance Endpoints

#### Clock In
```
POST /api/attendance/clock-in/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "employee_id": 1,
  "clock_in_time": "09:30:00",
  "date": "2026-01-16",
  "message": "Clocked in successfully"
}
```

#### Clock Out
```
POST /api/attendance/clock-out/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "employee_id": 1,
  "clock_out_time": "18:30:00",
  "date": "2026-01-16",
  "message": "Clocked out successfully"
}
```

#### Get My Attendance
```
GET /api/attendance/my-attendance/
Authorization: Bearer <access_token>

Response:
[
  {
    "id": 1,
    "employee_id": 1,
    "date": "2026-01-16",
    "status": "present",
    "clock_in_time": "09:30:00",
    "clock_out_time": "18:30:00"
  }
]
```

#### Get Today's Attendance
```
GET /api/attendance/today-attendance/
Authorization: Bearer <access_token>

Response:
[
  {
    "id": 1,
    "employee_id": 1,
    "date": "2026-01-16",
    "status": "present",
    "clock_in_time": "09:30:00",
    "clock_out_time": null
  }
]
```

#### Submit Attendance Request
```
POST /api/attendance/attendance-request/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "request_type": "late_come",
  "date": "2026-01-16",
  "from_time": "10:00:00",
  "to_time": "11:00:00",
  "reason": "Traffic"
}

Response:
{
  "id": 1,
  "employee_id": 1,
  "request_type": "late_come",
  "date": "2026-01-16",
  "status": "pending"
}
```

### Payroll Endpoints

#### Get Payslips
```
GET /api/payroll/payslip/?page=1
Authorization: Bearer <access_token>

Response:
{
  "results": [
    {
      "id": 1,
      "employee_id": 1,
      "month": "2025-12",
      "gross_salary": 5000,
      "deductions": 500,
      "net_salary": 4500,
      "created_at": "2025-12-01"
    }
  ],
  "count": 12
}
```

### Leave Endpoints

#### Get Leave Requests
```
GET /api/leave/leave-request/?page=1
Authorization: Bearer <access_token>

Response:
{
  "results": [
    {
      "id": 1,
      "employee_id": 1,
      "leave_type": "annual",
      "from_date": "2026-01-15",
      "to_date": "2026-01-20",
      "status": "pending",
      "reason": "Vacation"
    }
  ],
  "count": 10
}
```

## Testing the Integration

### Step 1: Start Backend

```bash
cd /path/to/horilla-talent
python manage.py runserver 0.0.0.0:8000
```

Verify at `http://localhost:8000/api/` (should show API root)

### Step 2: Start Frontend

```bash
cd horilla-frontend
npm run dev
```

Verify at `http://localhost:3000`

### Step 3: Test Login

1. Navigate to `http://localhost:3000/login`
2. Enter valid Django username and password
3. Should redirect to dashboard on successful login
4. Check browser DevTools → Application → LocalStorage for stored tokens

### Step 4: Test API Calls

1. Go to `http://localhost:3000/employees`
2. Should load employee list from backend
3. Check browser DevTools → Network tab to verify API calls
4. Should see `Authorization: Bearer <token>` in request headers

### Step 5: Test Token Refresh

1. Get access token from localStorage
2. Manually delete the token
3. Wait for token to expire (or manually set expired date)
4. Make another API request
5. Should automatically refresh token without user interaction

### Step 6: Test Error Handling

1. Stop Django backend
2. Try to make API call from frontend
3. Should show error message
4. Check Network tab for failed requests

## Troubleshooting

### CORS Error

**Error**: `Access to XMLHttpRequest at 'http://localhost:8000/...' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
1. Check Django `settings.py` has `CORS_ALLOWED_ORIGINS`
2. Verify frontend URL is included
3. Check `corsheaders` is installed and in MIDDLEWARE
4. Clear browser cache
5. Restart Django backend

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Authentication Failed

**Error**: Login returns 401 or credentials not accepted

**Solution**:
1. Verify user exists in Django admin
2. Check JWT is properly configured
3. Verify `simplejwt` is installed
4. Check token endpoints are in API URLs
5. Test with curl:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

### API Endpoints Not Found

**Error**: 404 errors when calling API endpoints

**Solution**:
1. Verify `horilla_api` is in `INSTALLED_APPS`
2. Check URL routing in `horilla/urls.py`
3. Verify API URL prefix: `path('api/', include('horilla_api.urls'))`
4. Check endpoint exists in relevant app's API views
5. Test with:
```bash
curl http://localhost:8000/api/
```

### Token Expiration Issues

**Error**: Keep getting 401 errors after login

**Solution**:
1. Check JWT token lifetime:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

2. Verify refresh endpoint works:
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

3. Check API client interceptor in `utils/api-client.ts`

### Requests Missing Authorization Header

**Error**: API returns 401, but user is logged in

**Solution**:
1. Check localStorage has tokens:
```javascript
console.log(localStorage.getItem('auth:access_token'))
```

2. Verify API client interceptor adds header:
```typescript
// In utils/api-client.ts
const token = authStore.accessToken
if (token) {
  config.headers.Authorization = `Bearer ${token}`
}
```

3. Check auth store is initialized:
```javascript
const authStore = useAuthStore()
console.log(authStore.isAuthenticated)
```

### Database Connection Issues

**Error**: Backend shows database connection errors

**Solution**:
1. Check PostgreSQL is running (if used)
2. Verify database credentials in `.env`
3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

### Port Already in Use

**Error**: Port 8000 or 3000 already in use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 0.0.0.0:8001
npm run dev -- -p 3001
```

## Next Steps

1. **Customize Components**: Modify components in `components/` directory
2. **Add More Pages**: Create new pages for additional modules
3. **Styling**: Customize colors and theme in `tailwind.config.ts`
4. **Testing**: Add unit and integration tests
5. **Deployment**: Deploy frontend and backend to production

## Support

For issues with integration:
1. Check browser console for errors
2. Check Network tab for failed requests
3. Check Django logs for backend errors
4. Review this guide for common solutions
5. Check API endpoint documentation

---

**Last Updated**: January 2026
