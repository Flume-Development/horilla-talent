# Horilla Frontend - Quick Start Guide

Get your Nuxt 4 frontend running in minutes!

## Prerequisites

- Node.js 18+ installed
- Django backend running on `http://localhost:8000`

## Installation (2 minutes)

```bash
# Navigate to frontend directory
cd horilla-frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

The frontend will be available at **`http://localhost:3000`**

## Login

1. Open `http://localhost:3000` in your browser
2. You'll be redirected to login page
3. Use your Django admin credentials:
   - Username: `admin` (or your Django user)
   - Password: `admin` (or your Django password)
4. Click "Sign In"

## What's Included

### Pages
- ✅ **Login** - Authentication page
- ✅ **Dashboard** - Overview with stats and quick actions
- ✅ **Employees** - Employee directory and management
- ✅ **Attendance** - Clock in/out and attendance records
- ✅ **Leave** - Leave balance and requests
- ✅ **Payroll** - Salary slips and components

### Features
- 🔐 JWT-based authentication
- 📱 Responsive mobile design
- 🌙 Dark mode support
- 🎨 Tailwind CSS v4 styling
- 📊 Dashboard with statistics
- ⚡ Real-time API integration
- 🛡️ Route protection with middleware

### Components
- Sidebar navigation with user menu
- Top navigation bar
- Dashboard stat cards
- Data tables with filtering
- Form components
- Status badges

### Composables (Reusable Logic)
- `useApi()` - Generic API fetching
- `useEmployee()` - Employee operations
- `useAttendance()` - Attendance operations
- `useAuthStore()` - Authentication state

## Project Structure

```
horilla-frontend/
├── pages/          # Page components (auto-routed)
├── components/     # Reusable components
├── composables/    # Reusable logic
├── stores/         # Pinia state management
├── layouts/        # Page layouts
├── utils/          # Helper functions
├── assets/         # CSS and static files
├── middleware/     # Route middleware
└── plugins/        # Nuxt plugins
```

## Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Generate static site
npm run generate
```

## Environment Variables

Edit `.env.local` to configure:

```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000

# Development
NODE_ENV=development
NUXT_PORT=3000
```

## Connecting to Django Backend

### Verify Backend is Running

```bash
# Check if Django is running
curl http://localhost:8000/api/

# Should return API root information
```

### Update API Base URL (if needed)

If your Django backend runs on a different host:

```env
# .env.local
NUXT_PUBLIC_API_BASE_URL=http://your-backend-host:8000
```

### CORS Configuration

Ensure Django has CORS enabled:

```python
# horilla/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]
```

## Key Files to Know

| File | Purpose |
|------|---------|
| `nuxt.config.ts` | Nuxt configuration |
| `tailwind.config.ts` | Tailwind CSS configuration |
| `utils/api-client.ts` | API HTTP client |
| `stores/auth.ts` | Authentication state |
| `middleware/auth.ts` | Route protection |
| `pages/login.vue` | Login page |
| `pages/dashboard.vue` | Dashboard page |
| `layouts/default.vue` | Main layout with sidebar |

## Common Tasks

### Add a New Page

```vue
<!-- pages/my-page.vue -->
<template>
  <div>
    <h1>My Page</h1>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})
</script>
```

### Call an API Endpoint

```typescript
import { apiClient } from '~/utils/api-client'

// GET request
const data = await apiClient.get('/employee/employees/')

// POST request
const result = await apiClient.post('/employee/employees/', {
  first_name: 'John',
  last_name: 'Doe'
})
```

### Use Composable

```typescript
import { useEmployee } from '~/composables/useEmployee'

const { getEmployees, isLoading } = useEmployee()

const employees = await getEmployees(1, 10)
```

### Add Protected Route

```typescript
// In page component
definePageMeta({
  middleware: 'auth'
})
```

### Access Auth State

```typescript
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

// Check if authenticated
if (authStore.isAuthenticated) {
  console.log('User is logged in')
}

// Get current user
console.log(authStore.employee)

// Logout
authStore.logout()
```

## Troubleshooting

### Port Already in Use

```bash
npm run dev -- -p 3001
```

### Module Not Found Error

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API Connection Failed

1. Check Django backend is running: `curl http://localhost:8000/api/`
2. Check CORS is enabled in Django settings
3. Verify `NUXT_PUBLIC_API_BASE_URL` in `.env.local`
4. Check browser Network tab for failed requests

### Styling Issues

```bash
# Rebuild Tailwind CSS
npm run build
```

### Dark Mode Not Working

Clear browser cache and localStorage, then refresh.

## Next Steps

1. **Read Full Documentation**: See `README.md` for detailed documentation
2. **Integration Guide**: See `INTEGRATION_GUIDE.md` for backend integration details
3. **Customize Styling**: Edit `tailwind.config.ts` and `assets/css/main.css`
4. **Add More Pages**: Create new page components in `pages/`
5. **Deploy**: Build and deploy to production

## Useful Links

- [Nuxt 4 Documentation](https://nuxt.com)
- [Nuxt UI Documentation](https://ui.nuxt.com)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Pinia Documentation](https://pinia.vuejs.org)
- [Django REST Framework Docs](https://www.django-rest-framework.org/)

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review `INTEGRATION_GUIDE.md` for backend integration issues
3. Check `README.md` for detailed documentation
4. Review browser console for error messages
5. Check Network tab for failed API requests

---

**Version**: 1.0.0
**Last Updated**: January 2026
