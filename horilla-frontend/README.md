# Horilla Frontend - Nuxt 4 Application

A modern, responsive HR management system frontend built with **Nuxt 4**, **Nuxt UI 4**, and **Tailwind CSS v4**. This application integrates seamlessly with the Django REST API backend.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Development](#development)
- [Building for Production](#building-for-production)
- [API Integration](#api-integration)
- [Authentication](#authentication)
- [Modules](#modules)
- [Components](#components)
- [Composables](#composables)
- [Stores](#stores)
- [Deployment](#deployment)

## Features

- ✨ Modern, responsive user interface
- 🔐 JWT-based authentication with token refresh
- 👥 Employee management and directory
- ⏰ Attendance tracking with clock in/out
- 📅 Leave request management
- 💰 Payroll and salary slip viewing
- 📊 Dashboard with quick stats and activities
- 🌙 Dark mode support
- 📱 Mobile-responsive design
- 🚀 Server-side rendering with Nuxt 4
- 🎨 Tailwind CSS v4 with custom styling

## Tech Stack

- **Framework**: Nuxt 4
- **UI Library**: Nuxt UI 4
- **CSS Framework**: Tailwind CSS v4
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Build Tool**: Vite
- **Language**: TypeScript

## Project Structure

```
horilla-frontend/
├── app.vue                    # Root component
├── nuxt.config.ts             # Nuxt configuration
├── tailwind.config.ts         # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── package.json               # Dependencies
│
├── app/                       # App-level files
│
├── pages/                     # Page components (auto-routed)
│   ├── login.vue             # Login page
│   ├── dashboard.vue         # Dashboard
│   ├── employees/
│   │   ├── index.vue         # Employees list
│   │   └── [id].vue          # Employee details
│   ├── attendance/
│   │   ├── index.vue         # Attendance records
│   │   └── request.vue       # Request form
│   ├── leave/                # Leave management
│   ├── payroll/              # Payroll management
│   └── profile.vue           # User profile
│
├── components/               # Reusable Vue components
│   ├── SidebarNavigation.vue # Sidebar menu
│   ├── TopNavigation.vue     # Top navigation bar
│   ├── DashboardCard.vue     # Dashboard stat card
│   └── ...
│
├── layouts/                  # Layout components
│   ├── default.vue          # Main layout with sidebar
│   └── blank.vue            # Blank layout for login
│
├── composables/             # Reusable composition functions
│   ├── useApi.ts            # Generic API composable
│   ├── useEmployee.ts       # Employee API operations
│   ├── useAttendance.ts     # Attendance API operations
│   └── ...
│
├── stores/                  # Pinia state management
│   ├── auth.ts              # Authentication store
│   └── ...
│
├── utils/                   # Utility functions
│   ├── api-client.ts        # Axios API client
│   └── ...
│
├── middleware/              # Route middleware
│   └── auth.ts              # Authentication middleware
│
├── plugins/                 # Nuxt plugins
│
├── assets/                  # Static assets
│   └── css/
│       └── main.css        # Global styles
│
├── public/                  # Public static files
│
├── server/                  # Server routes (API routes)
│
└── .env.example             # Environment variables template
```

## Installation

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- The Horilla Django backend running on `http://localhost:8000`

### Setup Steps

1. **Navigate to the frontend directory**:
   ```bash
   cd horilla-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env.local
   ```

4. **Update environment variables** in `.env.local`:
   ```env
   NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NUXT_PORT=3000
   ```

5. **Start development server**:
   ```bash
   npm run dev
   ```

6. **Open in browser**:
   Navigate to `http://localhost:3000`

## Configuration

### Environment Variables

Create a `.env.local` file in the project root:

```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000

# Development
NODE_ENV=development
NUXT_PORT=3000

# Features
NUXT_PUBLIC_ENABLE_FACE_DETECTION=true
NUXT_PUBLIC_ENABLE_GEOFENCING=true
```

### Nuxt Configuration

Edit `nuxt.config.ts` to customize:
- API base URL and timeout
- UI components
- CSS framework
- Build settings

### Tailwind Configuration

Customize `tailwind.config.ts` for:
- Custom colors
- Font families
- Theme extensions
- Plugins

## Development

### Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Hot Module Replacement

Changes are automatically reflected in the browser thanks to HMR.

### Type Checking

```bash
npm run type-check
```

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

### Generate Static Site

```bash
npm run generate
```

## API Integration

### API Client

The `apiClient` utility handles all HTTP requests to the Django backend:

```typescript
// Located in: utils/api-client.ts
import { apiClient } from '~/utils/api-client'

// GET request
const data = await apiClient.get('/employees/')

// POST request
const result = await apiClient.post('/employees/', { name: 'John' })

// PUT request
await apiClient.put('/employees/1/', { name: 'Jane' })

// DELETE request
await apiClient.delete('/employees/1/')
```

### Base URL

The API base URL is configured in `nuxt.config.ts` and can be overridden via `.env.local`:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Authentication

### Login Flow

1. User submits credentials on login page
2. Credentials are sent to `/api/auth/login/`
3. Backend returns `access_token`, `refresh_token`, and employee data
4. Tokens and user data are stored in localStorage
5. `access_token` is included in Authorization header for all API requests

### Token Refresh

- When API returns 401 (Unauthorized), automatic token refresh is attempted
- Uses `refresh_token` to obtain new `access_token`
- If refresh fails, user is redirected to login page

### Auth Store

Located in `stores/auth.ts`:

```typescript
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

// Check authentication status
authStore.isAuthenticated

// Get current user
authStore.employee

// Login
await authStore.login(username, password)

// Logout
authStore.logout()

// Refresh token
await authStore.refreshAccessToken()
```

## Modules

### Dashboard Module

**Pages**: `/dashboard`

- Overview of system statistics
- Quick attendance actions (Clock in/out)
- Recent activities
- Quick access links

### Employees Module

**Pages**: `/employees`, `/employees/[id]`, `/employees/create`

**Composable**: `useEmployee.ts`

Features:
- List all employees with filtering
- View employee details and work information
- Create new employees
- Update employee information
- Delete employees

### Attendance Module

**Pages**: `/attendance`, `/attendance/request`

**Composable**: `useAttendance.ts`

Features:
- Clock in/out operations
- View attendance records
- Filter by date and status
- Submit attendance requests (late, early out)
- View request status

### Leave Module

**Pages**: `/leave`, `/leave/request`

Features:
- View leave balance
- Request leave
- View leave history
- Track leave approvals

### Payroll Module

**Pages**: `/payroll`, `/payroll/[id]`

Features:
- View payslips
- Download payslips
- View salary components
- Manage loans and reimbursements

## Components

### Global Components

All components in the `components/` directory are auto-imported.

**Key Components**:

- **SidebarNavigation.vue**: Main sidebar with navigation menu
- **TopNavigation.vue**: Top bar with breadcrumbs and actions
- **DashboardCard.vue**: Stat card for dashboard

### Creating Components

```vue
<!-- components/MyComponent.vue -->
<template>
  <div>Component content</div>
</template>

<script setup lang="ts">
// Component logic
</script>
```

Use in pages:
```vue
<template>
  <MyComponent />
</template>
```

## Composables

Composables are reusable logic functions for Vue components.

### useApi

Generic API data fetching composable:

```typescript
import { useApi } from '~/composables/useApi'

const { data, isLoading, error, execute } = useApi('/employees/')
```

### useEmployee

Employee operations:

```typescript
import { useEmployee } from '~/composables/useEmployee'

const { getEmployees, getEmployeeById, createEmployee, updateEmployee, deleteEmployee } = useEmployee()

// Fetch all employees
const response = await getEmployees(page, limit)

// Get specific employee
const employee = await getEmployeeById(1)

// Create employee
const newEmployee = await createEmployee({ first_name: 'John', ... })

// Update employee
await updateEmployee(1, { last_name: 'Doe' })

// Delete employee
await deleteEmployee(1)
```

### useAttendance

Attendance operations:

```typescript
import { useAttendance } from '~/composables/useAttendance'

const { clockIn, clockOut, getMyAttendance, submitAttendanceRequest } = useAttendance()

// Clock in
await clockIn()

// Clock out
await clockOut()

// Get my records
const records = await getMyAttendance()

// Submit request
await submitAttendanceRequest({ request_type: 'late_come', ... })
```

## Stores

### Auth Store

Pinia store for authentication state:

```typescript
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

// State
authStore.accessToken
authStore.refreshToken
authStore.employee
authStore.isAuthenticated
authStore.isLoading
authStore.error

// Methods
await authStore.login(username, password)
authStore.logout()
await authStore.refreshAccessToken()
await authStore.checkAuthStatus()
```

## Middleware

### auth.ts

Protects routes from unauthenticated access:

```typescript
// Add to page metadata to protect route
definePageMeta({
  middleware: 'auth'
})
```

Public routes (no authentication required):
- `/login`
- `/forgot-password`
- `/register`

## Deployment

### Production Build

```bash
npm run build
```

Creates optimized build in `.output` directory.

### Environment Variables for Production

Update `.env.local` or set via hosting platform:

```env
NUXT_PUBLIC_API_BASE_URL=https://api.horilla.com
NODE_ENV=production
NUXT_DEPLOYMENT_URL=https://hr.horilla.com
```

### Deploy to Vercel

1. Push to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

### Deploy to Other Platforms

The application can be deployed to any platform that supports Node.js 18+:
- Netlify
- AWS Amplify
- Railway
- Render
- Docker

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

ENV HOST=0.0.0.0
EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
```

```bash
docker build -t horilla-frontend .
docker run -p 3000:3000 -e NUXT_PUBLIC_API_BASE_URL=http://backend:8000 horilla-frontend
```

## API Endpoints Reference

The frontend communicates with these Django API endpoints:

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/token/refresh/` - Refresh token

### Employee
- `GET /api/employee/employees/` - List employees
- `GET /api/employee/employees/<id>/` - Get employee details
- `POST /api/employee/employees/` - Create employee
- `PUT /api/employee/employees/<id>/` - Update employee
- `DELETE /api/employee/employees/<id>/` - Delete employee
- `GET /api/employee/employee-work-information/<id>/` - Work info

### Attendance
- `POST /api/attendance/clock-in/` - Clock in
- `POST /api/attendance/clock-out/` - Clock out
- `GET /api/attendance/my-attendance/` - My attendance
- `GET /api/attendance/attendance/` - All attendance
- `GET /api/attendance/today-attendance/` - Today's attendance
- `POST /api/attendance/attendance-request/` - Submit request
- `GET /api/attendance/attendance-request/` - View requests

### Base
- `GET /api/base/companies/` - List companies
- `GET /api/base/departments/` - List departments
- `GET /api/base/job-positions/` - List job positions

### Payroll
- `GET /api/payroll/payslip/` - List payslips
- `GET /api/payroll/payslip/<id>/` - Get payslip

### Leave
- `GET /api/leave/leave-request/` - List leave requests
- `POST /api/leave/leave-request/` - Create leave request

## Troubleshooting

### API Connection Issues

1. Verify Django backend is running on configured URL
2. Check CORS settings in Django `settings.py`
3. Verify `CSRF_TRUSTED_ORIGINS` includes frontend URL
4. Check network tab in browser DevTools

### Authentication Issues

1. Clear localStorage and cookies
2. Check token expiry and refresh logic
3. Verify login endpoint returns proper token format
4. Check API response in browser DevTools

### Build Issues

1. Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
2. Clear `.nuxt` directory: `rm -rf .nuxt`
3. Update Node.js to latest LTS version

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Submit pull request with description

## License

[License type] - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Project Issues URL]
- Email: support@horilla.com

---

**Last Updated**: January 2026
