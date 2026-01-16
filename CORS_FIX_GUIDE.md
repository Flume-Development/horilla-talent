# CORS Integration Fix - Django Backend Configuration

## Problem

The frontend (http://localhost:3001) is being blocked by CORS policy when trying to connect to the Django backend (http://localhost:8000) for the login request:

```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/login/' from origin 'http://localhost:3001'
has been blocked by CORS policy: Response to preflight request doesn't pass access control check:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Solution Applied

The Django backend has been configured with the following changes to enable CORS and API support:

### 1. Updated `horilla/settings.py`

#### Added CORS Configuration
```python
# CORS Configuration for Frontend Integration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:8080",
]

CORS_ALLOW_CREDENTIALS = True
```

#### Added REST Framework Configuration
```python
# REST Framework Configuration
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
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}
```

#### Added JWT Token Configuration
```python
# JWT Token Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

#### Added Missing Apps to INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ... existing apps ...
    "rest_framework",
    "rest_framework_simplejwt",
    "horilla_api",
    # ... other apps ...
]
```

### 2. Updated `horilla/urls.py`

Added the API URL configuration:
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("horilla_api.urls")),  # ← Added this line
    path("accounts/", include("django.contrib.auth.urls")),
    # ... other patterns ...
]
```

### 3. Updated `.env` File

Added CSRF_TRUSTED_ORIGINS:
```env
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001,http://localhost:8080
```

## Next Steps to Complete Integration

### Step 1: Activate Virtual Environment

```bash
# Navigate to project root
cd /Users/omondiochieng/Repos/horilla-talent

# Create a virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install specific packages if no requirements file
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

### Step 3: Run Migrations

```bash
python manage.py migrate
```

### Step 4: Create Superuser (if needed)

```bash
python manage.py createsuperuser
```

### Step 5: Start Django Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The backend should now be running at **http://localhost:8000**

### Step 6: Start Nuxt Frontend (in separate terminal)

```bash
cd horilla-frontend
npm run dev
```

The frontend should now be running at **http://localhost:3001**

## Step 7: Test Integration

1. Open **http://localhost:3001/login** in your browser
2. Enter your Django admin credentials (username/password)
3. Click "Sign In"
4. You should be redirected to **http://localhost:3001/dashboard**

## Troubleshooting

### Still Getting CORS Errors?

1. **Check Django Server is Running**
   ```bash
   curl -i http://localhost:8000/api/
   ```
   Should return a response with headers

2. **Verify CORS Middleware is Active**
   - Check that `corsheaders` is in `INSTALLED_APPS`
   - Check that `CorsMiddleware` is in `MIDDLEWARE`
   - Check that it comes BEFORE `CommonMiddleware`

3. **Verify Settings are Loaded**
   ```bash
   python manage.py shell
   >>> from django.conf import settings
   >>> settings.CORS_ALLOWED_ORIGINS
   ['http://localhost:3000', 'http://localhost:3001', ...]
   ```

4. **Test CORS Directly**
   ```bash
   curl -H "Origin: http://localhost:3001" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        http://localhost:8000/api/auth/login/
   ```
   Should include `Access-Control-Allow-Origin` header in response

### API Endpoints Not Found?

If you get 404 errors on `/api/` endpoints:

1. Verify `horilla_api` is in `INSTALLED_APPS`
2. Verify `path("api/", include("horilla_api.urls"))` is in `urls.py`
3. Run migrations: `python manage.py migrate`
4. Restart Django server

### Login Returns 401/403?

1. Check that a valid user exists in Django admin
2. Ensure `rest_framework_simplejwt` is installed
3. Check JWT settings in `settings.py`
4. Try login with correct credentials

## API Endpoints Available

After configuration, the following endpoints should be available:

### Authentication
- `POST /api/auth/login/` - Login with username/password
- `POST /api/auth/token/refresh/` - Refresh access token

### Employee
- `GET /api/employee/employees/` - List employees
- `POST /api/employee/employees/` - Create employee
- `GET /api/employee/employees/{id}/` - Get employee details
- `PUT /api/employee/employees/{id}/` - Update employee
- `DELETE /api/employee/employees/{id}/` - Delete employee

### Attendance
- `POST /api/attendance/clock-in/` - Clock in
- `POST /api/attendance/clock-out/` - Clock out
- `GET /api/attendance/my-attendance/` - Get my attendance
- `GET /api/attendance/attendance/` - Get all attendance records

### Leave
- `GET /api/leave/leave-request/` - List leave requests
- `POST /api/leave/leave-request/` - Create leave request

### Payroll
- `GET /api/payroll/payslip/` - List payslips
- `POST /api/payroll/payslip/` - Create payslip

## Testing the Complete Integration

### Terminal 1: Start Backend
```bash
cd /Users/omondiochieng/Repos/horilla-talent
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Terminal 2: Start Frontend
```bash
cd /Users/omondiochieng/Repos/horilla-talent/horilla-frontend
npm run dev
```

### Terminal 3: Test with curl
```bash
# Test login endpoint
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Response should include access and refresh tokens
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "employee": {...}
# }
```

## Configuration Files Modified

| File | Changes |
|------|---------|
| `horilla/settings.py` | Added CORS, REST Framework, JWT, and missing apps |
| `horilla/urls.py` | Added API URL routing |
| `.env` | Added CSRF_TRUSTED_ORIGINS |

## Files NOT Modified (Already Correct)

- Frontend `/horilla-frontend/` - Fully functional and tested
- Frontend API client - Already configured for `/api` routes
- Frontend auth store - Already has token refresh logic

## Next: Full End-to-End Testing

Once the Django backend is properly set up and running with these configurations:

1. The CORS errors should be resolved
2. Frontend can authenticate with Django
3. All API endpoints become accessible
4. The full HR system is operational

---

**Last Updated**: January 16, 2026
**Status**: Configuration Complete - Awaiting Backend Startup
