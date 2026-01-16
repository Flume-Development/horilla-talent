# Horilla Frontend Setup & Integration

## 🎉 Frontend Successfully Created!

A complete Nuxt 4 frontend application has been created for the Horilla HR management system. This document provides an overview of what was built and how to get started.

## 📁 Project Location

```
/Users/omondiochieng/Repos/horilla-talent/horilla-frontend/
```

## ✨ What's Included

### Core Technologies
- **Nuxt 4** - Meta-framework for Vue 3
- **Vue 3** - Progressive JavaScript framework
- **Nuxt UI 4** - Nuxt UI components library
- **Tailwind CSS v4** - Utility-first CSS framework
- **Pinia** - State management
- **Axios** - HTTP client
- **TypeScript** - Type-safe JavaScript

### Features Implemented
✅ Authentication (JWT with token refresh)
✅ Dashboard with statistics and quick actions
✅ Employee management (CRUD operations)
✅ Attendance tracking (clock in/out)
✅ Leave management system
✅ Payroll management
✅ Dark mode support
✅ Responsive design
✅ Protected routes
✅ Global navigation

### Pages Created
- `/login` - Login page
- `/dashboard` - Dashboard with stats
- `/employees` - Employee directory
- `/employees/[id]` - Employee details
- `/attendance` - Attendance records
- `/leave` - Leave management
- `/payroll` - Payroll information

### Components Created
- `SidebarNavigation.vue` - Main sidebar with navigation
- `TopNavigation.vue` - Top bar with breadcrumbs
- `DashboardCard.vue` - Stat card component
- Auto-imported global components

### Composables Created
- `useApi.ts` - Generic data fetching
- `useEmployee.ts` - Employee API operations
- `useAttendance.ts` - Attendance API operations
- `useAuthStore` (Pinia) - Authentication state

### Utilities Created
- `api-client.ts` - Axios HTTP client with interceptors
  - Automatic token refresh
  - Error handling
  - Request/response logging

### Middleware Created
- `auth.ts` - Route protection middleware

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd horilla-frontend
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env.local
```

Update `.env.local`:
```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PORT=3000
```

### 3. Start Development Server
```bash
npm run dev
```

Visit `http://localhost:3000`

### 4. Login
Use your Django credentials to login

## 📚 Documentation Files

### Main Documentation
- **README.md** - Complete project documentation
  - Features overview
  - Project structure
  - Installation guide
  - API integration
  - Deployment instructions

### Quick References
- **QUICKSTART.md** - Get running in 5 minutes
  - Prerequisites
  - Installation
  - Common tasks
  - Troubleshooting

- **INTEGRATION_GUIDE.md** - Django backend integration
  - Backend setup
  - API endpoints
  - CORS configuration
  - Authentication flow
  - Testing integration

## 🔧 Project Structure

```
horilla-frontend/
├── app.vue                    # Root component
├── nuxt.config.ts             # Nuxt configuration
├── tailwind.config.ts         # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── package.json               # Dependencies
├── Dockerfile                 # Docker containerization
├── docker-compose.yml         # Docker Compose setup
│
├── pages/                     # Page components (auto-routed)
│   ├── login.vue             # Login page
│   ├── dashboard.vue         # Dashboard
│   ├── employees/            # Employee management
│   ├── attendance/           # Attendance tracking
│   ├── leave/                # Leave management
│   └── payroll/              # Payroll information
│
├── components/               # Reusable Vue components
│   ├── SidebarNavigation.vue
│   ├── TopNavigation.vue
│   ├── DashboardCard.vue
│
├── layouts/                  # Layout components
│   ├── default.vue          # Main layout with sidebar
│   └── blank.vue            # Blank layout for login
│
├── composables/             # Reusable logic
│   ├── useApi.ts
│   ├── useEmployee.ts
│   └── useAttendance.ts
│
├── stores/                  # Pinia state management
│   └── auth.ts              # Authentication store
│
├── utils/                   # Utilities
│   └── api-client.ts        # API HTTP client
│
├── middleware/              # Route middleware
│   └── auth.ts              # Authentication middleware
│
├── plugins/                 # Nuxt plugins
│   └── auth.ts              # Auth initialization
│
├── assets/                  # Static assets
│   └── css/
│       └── main.css        # Global styles
│
├── README.md                # Full documentation
├── QUICKSTART.md            # Quick start guide
├── INTEGRATION_GUIDE.md     # Django integration
├── .env.example             # Environment template
└── .gitignore               # Git ignore rules
```

## 📋 Available Scripts

```bash
# Development
npm run dev              # Start dev server on port 3000

# Production
npm run build            # Build for production
npm run preview          # Preview production build
npm run generate         # Generate static site

# Development tools
npm run lint             # Run linter
npm run type-check       # Type checking (if available)
```

## 🔌 API Integration

The frontend automatically connects to the Django backend at `http://localhost:8000`.

### Authentication Flow
1. User logs in with credentials
2. Frontend receives JWT access and refresh tokens
3. Tokens stored in localStorage
4. All API requests include Authorization header
5. Expired tokens automatically refreshed

### Supported Endpoints
- `POST /api/auth/login/` - Login
- `GET /api/employee/employees/` - List employees
- `GET /api/employee/employees/{id}/` - Employee details
- `POST /api/attendance/clock-in/` - Clock in
- `POST /api/attendance/clock-out/` - Clock out
- `GET /api/attendance/my-attendance/` - My attendance
- `GET /api/leave/leave-request/` - Leave requests
- `GET /api/payroll/payslip/` - Payslips

See `INTEGRATION_GUIDE.md` for complete endpoint documentation.

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t horilla-frontend .
```

### Run with Docker
```bash
docker run -p 3000:3000 \
  -e NUXT_PUBLIC_API_BASE_URL=http://backend:8000 \
  horilla-frontend
```

### Docker Compose (Frontend + Backend)
```bash
docker-compose up
```

Access frontend at `http://localhost:3000`

## 🛠️ Configuration

### Environment Variables
Create `.env.local`:

```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000

# Development
NODE_ENV=development
NUXT_PORT=3000
NUXT_HOST=0.0.0.0

# Feature Flags
NUXT_PUBLIC_ENABLE_FACE_DETECTION=true
NUXT_PUBLIC_ENABLE_GEOFENCING=true
```

### Tailwind Customization
Edit `tailwind.config.ts`:
- Custom colors
- Font families
- Spacing
- Theme extensions

### Nuxt Configuration
Edit `nuxt.config.ts`:
- API timeout
- Build settings
- Module configurations
- CSS imports

## 🧪 Testing Integration

1. **Start Backend**
   ```bash
   cd ../
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Start Frontend**
   ```bash
   cd horilla-frontend
   npm run dev
   ```

3. **Login**
   - Navigate to `http://localhost:3000`
   - Use Django credentials
   - Should redirect to dashboard

4. **Test API Calls**
   - Go to `/employees` page
   - Should load employee list from backend
   - Check Network tab for API calls

## 📱 Features Overview

### Authentication
- Login with username/password
- JWT token-based authentication
- Automatic token refresh
- Remember me functionality
- Secure token storage

### Dashboard
- Welcome message with user name
- Quick statistics cards
  - Total employees
  - Present today
  - On leave
  - Pending requests
- Attendance status
- Quick action buttons
- Recent activities timeline

### Employee Management
- List all employees with pagination
- Search and filter by name/email
- View employee details
- Create new employees
- Update employee information
- Delete employees
- Responsive table design

### Attendance
- Clock in/out functionality
- View attendance records
- Filter by date and status
- Submit attendance requests
- Request approval tracking
- Duration calculation

### Leave Management
- View leave balance
- Request new leave
- Track leave status
- View leave history
- Multiple leave types

### Payroll
- View current month salary
- Salary breakdown (earnings/deductions)
- Recent payslips
- Download payslips
- View salary history

## 🌙 Dark Mode

Dark mode is fully supported with:
- Toggle button in top navigation
- Persistent preference (localStorage)
- Tailwind dark mode classes
- All components styled for dark mode

## ♿ Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast compliance
- Focus indicators

## 🔐 Security Features

- JWT authentication
- Token refresh mechanism
- Secure token storage
- CORS enabled
- Protected routes
- Input validation
- XSS protection (Vue 3)

## 🚢 Deployment

### To Vercel
1. Push to GitHub
2. Connect to Vercel
3. Set environment variables
4. Deploy

### To Other Platforms
- Netlify, AWS Amplify, Railway, etc.
- Set `NUXT_PUBLIC_API_BASE_URL` to production backend
- Run `npm run build` then `npm run preview`

## 📞 Support & Documentation

### Quick Links
- **README.md** - Full documentation
- **QUICKSTART.md** - 5-minute setup
- **INTEGRATION_GUIDE.md** - Backend integration

### Troubleshooting
All common issues and solutions documented in:
1. QUICKSTART.md (Troubleshooting section)
2. INTEGRATION_GUIDE.md (Troubleshooting section)
3. README.md (Troubleshooting section)

### Browser DevTools
- Use Network tab to debug API calls
- Use Application/Storage tab to check tokens
- Use Console for error messages

## 🎓 Learning Resources

### Official Documentation
- [Nuxt 4](https://nuxt.com)
- [Vue 3](https://vuejs.org)
- [Nuxt UI](https://ui.nuxt.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Pinia](https://pinia.vuejs.org)

### Tutorials
- Check component files for examples
- Check pages for integration examples
- Check composables for reusable logic

## 📝 Next Steps

1. **Customize Branding**
   - Update logo in components
   - Customize colors in tailwind.config.ts
   - Update app title

2. **Add More Pages**
   - Create new pages in pages/ directory
   - Use existing components as templates
   - Add to navigation menu

3. **Implement Additional Features**
   - Add form validations
   - Add data export functionality
   - Add reporting features
   - Add notifications system

4. **Test Thoroughly**
   - Test all pages and flows
   - Test on mobile devices
   - Test error scenarios
   - Test dark mode

5. **Deploy**
   - Build for production: `npm run build`
   - Deploy to your hosting platform
   - Monitor logs and errors
   - Set up CI/CD pipeline

## ✅ Verification Checklist

Before going to production:

- [ ] All pages load correctly
- [ ] Login works with Django credentials
- [ ] API calls are successful (check Network tab)
- [ ] Dark mode toggle works
- [ ] Mobile responsive design works
- [ ] Token refresh works (wait for expiry)
- [ ] Navigation between pages works
- [ ] Error messages display correctly
- [ ] Performance is acceptable
- [ ] No console errors
- [ ] Environment variables configured
- [ ] CORS enabled on backend

## 🎉 You're All Set!

The Nuxt 4 frontend is ready to use! Follow the Quick Start guide above to get running.

For detailed information, refer to the documentation files included in the project.

---

**Frontend Version**: 1.0.0
**Created**: January 2026
**Framework**: Nuxt 4 with Vue 3, Nuxt UI 4, Tailwind CSS v4
**Backend**: Django REST Framework
