# Horilla Frontend - Performance Management System (PMS) UI

A modern Nuxt 4 frontend application for the Horilla Talent management system's Performance Management System (PMS) module. This frontend connects to the Django backend API to manage objectives, key results, feedback cycles, meetings, and bonus points.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Development](#development)
- [Building](#building)
- [API Integration](#api-integration)
- [Components](#components)
- [Composables](#composables)
- [State Management](#state-management)

## ✨ Features

### Objectives & Key Results (OKR)
- Create, view, and manage company and team objectives
- Assign objectives to employees
- Track key results and progress
- Monitor objective status (On Track, Behind, At Risk, Closed, Not Started)
- Update progress in real-time

### 360-Degree Feedback
- Create feedback cycles with multiple feedback sources
- Manage question templates and feedback questions
- Support for various question types (Text, Rating, Boolean, Multi-choice, Likert)
- Submit and view feedback responses
- Anonymous feedback collection

### Meetings
- Schedule and manage performance meetings
- Use question templates in meetings
- Collect employee responses
- View meeting answers and results

### Bonus Points Management
- Configure bonus point rules
- Award bonus points to employees
- Track employee bonus points

### Dashboard
- Performance overview with key metrics
- Status distribution charts
- Quick access to recent objectives and feedback
- Progress visualization

## 🛠 Tech Stack

- **Framework**: Nuxt 4 (Vue 3)
- **UI Framework**: Nuxt UI with Tailwind CSS v4
- **State Management**: Pinia
- **API Client**: Axios with JWT authentication
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4

## 📁 Project Structure

```
horilla-frontend/
├── assets/
│   └── css/
│       └── main.css              # Global Tailwind CSS styles
├── components/
│   ├── SidebarNavigation.vue      # Main sidebar navigation
│   ├── TopNavigation.vue          # Top navigation bar
│   ├── NavLink.vue                # Navigation link component
│   └── pms/
│       ├── dashboard/
│       │   └── StatCard.vue       # Statistics card component
│       ├── objectives/            # Objectives components
│       ├── feedback/              # Feedback components
│       ├── meetings/              # Meetings components
│       ├── bonus/                 # Bonus points components
│       └── shared/                # Shared PMS components
├── composables/
│   ├── usePms.ts                  # Core PMS composable
│   ├── useObjectives.ts           # Objectives management composable
│   ├── useFeedback.ts             # Feedback management composable
│   └── useMeetings.ts             # Meetings management composable
├── layouts/
│   ├── default.vue                # Main app layout with sidebar
│   └── blank.vue                  # Blank layout (for login, etc.)
├── middleware/
│   └── auth.ts                    # Authentication middleware
├── pages/
│   ├── login.vue                  # Login page
│   └── pms/
│       ├── index.vue              # PMS dashboard
│       ├── objectives/            # Objectives pages
│       ├── feedback/              # Feedback pages
│       ├── meetings/              # Meetings pages
│       └── bonus/                 # Bonus points pages
├── plugins/
│   └── auth.ts                    # Auth plugin (optional)
├── stores/
│   ├── auth.ts                    # Authentication store (Pinia)
│   └── pms.ts                     # PMS state store (Pinia)
├── types/
│   └── pms.ts                     # TypeScript type definitions
├── utils/
│   └── api-client.ts              # Axios API client configuration
├── app.vue                        # Root Vue component
├── nuxt.config.ts                 # Nuxt configuration
├── tsconfig.json                  # TypeScript configuration
├── package.json                   # Dependencies and scripts
└── .env.example                   # Environment variables template
```

## 🚀 Installation

### Prerequisites
- Node.js 18+ and npm/yarn
- Horilla backend running on `http://localhost:8000`

### Steps

1. **Navigate to the frontend directory**
   ```bash
   cd horilla-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Create .env file**
   ```bash
   cp .env.example .env
   ```

## ⚙️ Configuration

### Environment Variables

Edit `.env` file and configure:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000
```

- `NUXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NUXT_PUBLIC_API_TIMEOUT`: API request timeout in milliseconds

## 👨‍💻 Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Development Features
- Hot module replacement (HMR)
- TypeScript type checking
- Tailwind CSS utilities

## 🔨 Building

### Production Build

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

## 🔌 API Integration

### Authentication Flow

1. User logs in with credentials
2. Backend returns JWT tokens (access & refresh)
3. Tokens stored in localStorage and cookies
4. API client automatically includes tokens in requests
5. Expired tokens automatically refreshed
6. 401 responses trigger re-login

### API Client Usage

The API client is configured in `utils/api-client.ts` and handles:
- Base URL configuration
- JWT authentication headers
- Token refresh logic
- Error handling
- Response transformation

### Example Usage in Composables

```typescript
import { apiClient } from '~/utils/api-client'

// GET request
const objectives = await apiClient.get<Objective[]>('/pms/objectives/')

// POST request
const newObjective = await apiClient.post<Objective>(
  '/pms/objectives/',
  objectiveData
)

// PUT request
const updated = await apiClient.put<Objective>(
  `/pms/objectives/${id}/`,
  updateData
)

// DELETE request
await apiClient.delete(`/pms/objectives/${id}/`)
```

## 🧩 Components

### Core Components
- **SidebarNavigation.vue**: Main navigation sidebar with user menu
- **TopNavigation.vue**: Top header bar with title and actions
- **NavLink.vue**: Reusable navigation link component

### Dashboard Components
- **StatCard.vue**: Statistics card showing metrics

### Planned Components (Implementation Ready)
- ObjectiveCard, ObjectiveForm, ObjectiveDetailView
- EmployeeObjectiveCard, EmployeeObjectiveForm
- KeyResultCard, KeyResultForm
- ProgressUpdateModal, ProgressBar
- FeedbackCard, FeedbackForm, FeedbackDetailView
- QuestionRenderer (for different question types)
- FeedbackAnswerForm, FeedbackAnswersView
- MeetingCard, MeetingForm, MeetingDetailView
- BonusSettingCard, BonusSettingForm
- StatusBadge, PeriodSelector, EmployeeSelector
- FilterPanel, DataTable, EmptyState

## 🪝 Composables

### usePms()
Core PMS utilities:
- `fetchDashboardStats()`: Get dashboard statistics
- `getStatusColor(status)`: Get color for status
- `calculateProgress(current, target)`: Calculate progress percentage
- `formatDate(dateString)`: Format date to readable format
- `isDateRangeActive(start, end)`: Check if date range is active
- `getDaysRemaining(endDate)`: Get days until end date

### useObjectives()
Objectives management:
- `fetchObjectives(filters)`: List objectives
- `fetchObjective(id)`: Get single objective
- `createObjective(data)`: Create new objective
- `updateObjective(id, data)`: Update objective
- `deleteObjective(id)`: Delete objective
- `archiveObjective(id)`: Archive objective
- `fetchEmployeeObjectives(filters)`: List employee objectives
- `updateEmployeeObjectiveStatus(id, status)`: Update status
- `fetchEmployeeKeyResults(filters)`: List key results
- `updateKeyResultProgress(id, currentValue)`: Update progress

### useFeedback()
Feedback management:
- `fetchFeedbackList(filters)`: List feedback cycles
- `fetchFeedback(id)`: Get single feedback
- `createFeedback(data)`: Create feedback
- `submitFeedbackAnswers(feedbackId, answers)`: Submit answers
- `fetchFeedbackAnswers(id)`: Get feedback answers
- `fetchQuestionTemplates()`: List templates
- `createQuestion(data)`: Create question
- `fetchQuestions(templateId)`: Get template questions

### useMeetings()
Meetings management:
- `fetchMeetings(filters)`: List meetings
- `fetchMeeting(id)`: Get single meeting
- `createMeeting(data)`: Create meeting
- `updateMeeting(id, data)`: Update meeting
- `submitMeetingAnswers(meetingId, answers)`: Submit answers
- `fetchMeetingAnswers(meetingId)`: Get meeting answers

## 📦 State Management

### Pinia Stores

#### useAuthStore()
Manages authentication state:
- `accessToken`, `refreshToken`: JWT tokens
- `employee`: Current user info
- `isAuthenticated`: Auth status
- `login(username, password)`: Login
- `logout()`: Logout
- `refreshAccessToken()`: Refresh token
- `checkAuthStatus()`: Verify auth

#### usePmsStore()
Manages PMS data state:
- Lists: objectives, employeeObjectives, feedbackList, meetingsList
- Selected items: selectedObjective, selectedFeedback, selectedMeeting
- Filters: objectiveStatusFilter, objectivePeriodFilter, feedbackStatusFilter
- Stats: objectiveStats, averageProgress
- Actions to add/update/remove items

## 📝 Page Structure

### Public Pages
- `/login` - Login page

### Protected Pages (Requires Authentication)
- `/pms` - Dashboard
- `/pms/objectives` - Objectives list
- `/pms/my-objectives` - Employee's objectives
- `/pms/feedback` - Feedback cycles
- `/pms/meetings` - Meetings
- `/pms/bonus/*` - Bonus points management

## 🔒 Security Features

- JWT authentication with token refresh
- Protected routes via middleware
- Automatic token refresh on 401
- Logout on token expiration
- CORS handling for API requests
- Secure token storage (localStorage + cookies)

## 🎨 Styling

- **Tailwind CSS v4**: Utility-first CSS framework
- **Custom PMS Styles**: Located in `assets/css/main.css`
- **Status Colors**: Color-coded status badges
- **Responsive Design**: Mobile-first approach

## 🚢 Deployment

### Build and Deploy

1. Build the application
   ```bash
   npm run build
   ```

2. Deploy the `dist` directory to your hosting service
   - Vercel, Netlify, AWS, or any static host
   - Ensure API_BASE_URL points to production backend

### Environment Setup for Production

```env
NUXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
NUXT_PUBLIC_API_TIMEOUT=30000
```

## 🐛 Troubleshooting

### CORS Errors
- Ensure Django backend has CORS configured
- Check `CORS_ALLOWED_ORIGINS` in Django settings
- Frontend should be in allowed origins

### 401 Unauthorized
- Clear localStorage and cookies
- Log in again
- Check token expiration in Django settings

### API Not Responding
- Verify backend is running on configured URL
- Check network tab in browser DevTools
- Verify API endpoint URLs match backend routes

## 📚 Additional Resources

- [Nuxt 4 Documentation](https://nuxt.com)
- [Vue 3 Documentation](https://vuejs.org)
- [Pinia Documentation](https://pinia.vuejs.org)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Axios Documentation](https://axios-http.com)

## 📄 License

This project is part of the Horilla suite. See the main project for license information.

## 🤝 Contributing

When adding new features:

1. Create components in appropriate directories
2. Use TypeScript for type safety
3. Follow existing code patterns
4. Update composables for API calls
5. Use Pinia store for state management
6. Apply Tailwind CSS for styling
7. Add documentation for new features

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Check backend logs for API errors
4. File an issue in the main Horilla project

---

**Last Updated**: January 2025
**Nuxt Version**: 4.0.0
**Vue Version**: 3.4.0
