# PMS API Testing & Integration Guide

## Overview

This guide provides instructions for testing the PMS (Performance Management System) API endpoints and integrating them with the Nuxt frontend application.

## Backend Setup

### Prerequisites
- Django 4.x installed
- Django REST Framework
- djangorestframework-simplejwt
- Django CORS Headers

### Starting the Backend Server

```bash
# Navigate to project root
cd /path/to/horilla-talent

# Apply migrations (if not done)
python manage.py migrate

# Create a superuser (if not done)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### CORS Configuration

Ensure these settings exist in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

## Frontend Setup

### Install Dependencies

```bash
cd horilla-frontend
npm install
```

### Environment Configuration

Create `.env` file in `horilla-frontend/`:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000
```

### Start Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## API Endpoints

### Base URL
```
http://localhost:8000/api/pms/
```

### Authentication Endpoints

**Login**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refresh Token**
```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### PMS Endpoints

#### Objectives

**List Objectives**
```bash
GET /api/pms/objectives/
Authorization: Bearer {access_token}
```

**Create Objective**
```bash
POST /api/pms/objectives/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Q1 Goals",
  "description": "First quarter objectives",
  "status": "Not Started",
  "duration": 3,
  "duration_unit": "months",
  "manager_ids": [1, 2]
}
```

**Get Objective Details**
```bash
GET /api/pms/objectives/{id}/
Authorization: Bearer {access_token}
```

**Update Objective**
```bash
PUT /api/pms/objectives/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "status": "On Track"
}
```

**Delete Objective**
```bash
DELETE /api/pms/objectives/{id}/
Authorization: Bearer {access_token}
```

**Archive Objective**
```bash
POST /api/pms/objectives/{id}/archive/
Authorization: Bearer {access_token}
```

#### Employee Objectives

**List Employee Objectives**
```bash
GET /api/pms/employee-objectives/
Authorization: Bearer {access_token}
```

**Update Employee Objective Status**
```bash
POST /api/pms/employee-objectives/{id}/status/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "On Track"
}
```

**Update Progress**
```bash
POST /api/pms/employee-key-results/{id}/progress/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "current_value": 75
}
```

#### Feedback

**List Feedback Cycles**
```bash
GET /api/pms/feedback/
Authorization: Bearer {access_token}
```

**Create Feedback Cycle**
```bash
POST /api/pms/feedback/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Q1 Feedback",
  "description": "First quarter feedback cycle",
  "status": "Not Started",
  "start_date": "2025-01-01",
  "end_date": "2025-03-31",
  "allow_anonymous": true
}
```

**Submit Feedback Answers**
```bash
POST /api/pms/feedback/{id}/submit-answers/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "answers": [
    {
      "question_id": 1,
      "answer": "Great performance"
    },
    {
      "question_id": 2,
      "answer": "5"
    }
  ]
}
```

**Get Feedback Answers**
```bash
GET /api/pms/feedback/{id}/answers/
Authorization: Bearer {access_token}
```

#### Meetings

**List Meetings**
```bash
GET /api/pms/meetings/
Authorization: Bearer {access_token}
```

**Create Meeting**
```bash
POST /api/pms/meetings/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Performance Review",
  "description": "Q1 Performance Review Meeting",
  "status": "Scheduled",
  "meeting_date": "2025-02-15",
  "meeting_time": "14:00",
  "attendees": [1, 2, 3]
}
```

**Submit Meeting Answers**
```bash
POST /api/pms/meetings/{id}/submit-answers/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "answers": [
    {
      "question_id": 1,
      "answer": "Discussed Q1 performance"
    }
  ]
}
```

#### Bonus Points

**List Bonus Settings**
```bash
GET /api/pms/bonus-settings/
Authorization: Bearer {access_token}
```

**Create Bonus Setting**
```bash
POST /api/pms/bonus-settings/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Performance Bonus",
  "points": 10,
  "frequency": "monthly"
}
```

**List Employee Bonus Points**
```bash
GET /api/pms/employee-bonus-points/
Authorization: Bearer {access_token}
```

**Award Bonus Points**
```bash
POST /api/pms/employee-bonus-points/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "employee_id": 1,
  "points": 50,
  "reason": "Excellent Q1 performance"
}
```

#### Dashboard

**Get Dashboard Statistics**
```bash
GET /api/pms/dashboard/stats/
Authorization: Bearer {access_token}
```

## Testing with cURL

### 1. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

Save the `access` token from the response.

### 2. Test Objectives Endpoint

```bash
# List objectives
curl -X GET http://localhost:8000/api/pms/objectives/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create objective
curl -X POST http://localhost:8000/api/pms/objectives/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q1 Goals",
    "description": "First quarter objectives",
    "status": "Not Started",
    "duration": 3,
    "duration_unit": "months",
    "manager_ids": [1]
  }'
```

### 3. Test Feedback Endpoint

```bash
curl -X POST http://localhost:8000/api/pms/feedback/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q1 Feedback",
    "description": "First quarter feedback",
    "status": "Not Started",
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "allow_anonymous": true
  }'
```

### 4. Test Dashboard

```bash
curl -X GET http://localhost:8000/api/pms/dashboard/stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing with Postman

1. Create a new collection called "Horilla PMS"
2. Create an environment with variables:
   - `base_url` = `http://localhost:8000/api`
   - `access_token` = (will be set after login)

3. Create requests for each endpoint
4. Use the login request to get the token and set it in the environment

## Frontend Integration Testing

### 1. Start Both Servers

```bash
# Terminal 1: Backend
python manage.py runserver

# Terminal 2: Frontend
cd horilla-frontend
npm run dev
```

### 2. Test Login Flow

1. Navigate to `http://localhost:3000/login`
2. Enter credentials (username: admin, password: your_password)
3. Check browser DevTools > Network to see auth requests
4. Verify token is stored in localStorage

### 3. Test Pages

Visit each page and verify data is loading:

- `http://localhost:3000/pms/` - Dashboard
- `http://localhost:3000/pms/objectives/` - Objectives List
- `http://localhost:3000/pms/objectives/create` - Create Objective
- `http://localhost:3000/pms/my-objectives` - My Objectives
- `http://localhost:3000/pms/feedback/` - Feedback Cycles
- `http://localhost:3000/pms/feedback/create` - Create Feedback
- `http://localhost:3000/pms/meetings/` - Meetings
- `http://localhost:3000/pms/meetings/create` - Schedule Meeting
- `http://localhost:3000/pms/bonus/` - Bonus Points

### 4. Check Network Requests

1. Open Browser DevTools (F12)
2. Go to Network tab
3. Perform actions and verify:
   - Status code is 200/201
   - Response contains expected data
   - Authorization header is sent
   - Token refresh works when token expires

### 5. Handle Errors

Look for error states:
- Invalid credentials → Red error message on login
- 401 Unauthorized → Automatic logout and redirect to login
- Network errors → Retry button appears
- Form validation errors → Inline error messages

## API Client Setup

The frontend uses `useApiClient()` composable which handles:
- Base URL configuration
- Token management
- Request/response interceptors
- Error handling
- Token auto-refresh

Usage in components:

```typescript
const apiClient = useApiClient()

// GET request
const objectives = await apiClient.get('/pms/objectives/')

// POST request
const newObjective = await apiClient.post('/pms/objectives/', {
  title: 'Q1 Goals',
  // ...
})

// PUT request
const updated = await apiClient.put('/pms/objectives/1/', {
  status: 'On Track'
})

// DELETE request
await apiClient.delete('/pms/objectives/1/')
```

## Debugging Tips

### Network Issues
- Check CORS headers in response
- Verify API_BASE_URL in .env
- Check if backend server is running

### Authentication Issues
- Verify token is in localStorage
- Check token expiration time
- Ensure Authorization header format: `Bearer {token}`

### Data Not Loading
- Check browser console for errors
- Verify API endpoint exists in backend
- Test endpoint with cURL first
- Check user has permission to access endpoint

### State Management
- Verify Pinia store is being updated
- Check composable functions return correct data
- Look for error messages in pmsStore.error

## Production Deployment

### Backend (Django)
```bash
# Collect static files
python manage.py collectstatic

# Use production server (gunicorn, uWSGI, etc.)
gunicorn horilla.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (Nuxt)
```bash
# Build
npm run build

# Serve with production server
npx nuxi preview
```

Update `.env` with production API URL:
```env
NUXT_PUBLIC_API_BASE_URL=https://your-api-domain.com
```

## Common Issues & Solutions

### Issue: CORS errors in browser console
**Solution:** Add frontend URL to `CORS_ALLOWED_ORIGINS` in Django settings

### Issue: 401 Unauthorized errors
**Solution:**
- Verify token is being sent
- Check token hasn't expired
- Verify user has required permissions

### Issue: API responses are empty
**Solution:**
- Check API endpoint implementation
- Verify database has data
- Check filtering/pagination parameters

### Issue: Form submissions fail silently
**Solution:**
- Check browser console for errors
- Verify required fields are filled
- Check API response status and error message

## Next Steps

1. ✅ Create remaining PMS pages
2. ✅ Build management components
3. Test all API endpoints with both cURL and frontend
4. Verify authentication and token refresh
5. Test error handling scenarios
6. Load test with sample data
7. Deploy to staging environment
8. Conduct user acceptance testing
9. Deploy to production

## Support

For issues or questions:
1. Check Django logs: `python manage.py` output
2. Check browser console: DevTools > Console
3. Check network requests: DevTools > Network
4. Review error messages in pmsStore.error
5. Consult Django REST Framework documentation

---

**Last Updated**: January 2025
**Version**: 1.0.0
