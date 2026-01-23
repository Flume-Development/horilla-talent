# Installation & Setup Guide

## Prerequisites

- Node.js 18+
- npm or yarn
- Horilla backend running on `http://localhost:8000`

## Quick Start

### 1. Install Dependencies

```bash
cd horilla-frontend
npm install
```

### 2. Configure Environment

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and ensure correct API settings:

```env
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
NUXT_PUBLIC_API_TIMEOUT=30000
```

### 3. Start Development Server

```bash
npm run dev
```

Access the application at: `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Create production build
- `npm run preview` - Preview production build
- `npm run generate` - Generate static site
- `npm run lint` - Run ESLint

## Backend Setup

Ensure your Django backend is running with PMS API endpoints:

```bash
# In horilla-talent directory
python manage.py migrate
python manage.py runserver
```

The backend should be accessible at `http://localhost:8000`

## Login

Default test credentials (if available in your setup):
- Username: `test` or your Django superuser username
- Password: Your Django superuser password

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, Nuxt will automatically use the next available port.

### Backend Connection Failed

- Verify Django backend is running
- Check `CORS_ALLOWED_ORIGINS` in Django settings
- Ensure `NUXT_PUBLIC_API_BASE_URL` matches your backend URL

### Clear Cache & Reinstall

```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### View Logs

Check browser console (F12) for frontend errors and terminal for build errors.

## Project Structure

```
horilla-frontend/
├── pages/           # Page components (routes)
├── components/      # Reusable Vue components
├── composables/     # Reusable composition functions
├── stores/          # Pinia state stores
├── types/           # TypeScript type definitions
├── utils/           # Utility functions
├── layouts/         # Layout templates
├── middleware/      # Route middleware
├── assets/          # Static assets & CSS
└── nuxt.config.ts   # Nuxt configuration
```

## Next Steps

1. **Customize Dashboard** - Edit `pages/pms/index.vue`
2. **Create Components** - Add components in `components/pms/`
3. **Add Pages** - Create new pages in `pages/pms/`
4. **Extend API** - Use composables in `composables/`
5. **Deploy** - Build and deploy to your hosting

## Support

For issues:
1. Check browser DevTools console
2. Verify backend is running
3. Check Django logs for API errors
4. Ensure environment variables are set correctly

## Production Deployment

### Build

```bash
npm run build
```

### Deploy

The `dist` directory contains the production build. Deploy to:
- Vercel
- Netlify
- AWS
- Any static host

Remember to set environment variables in production!

---

**Last Updated**: January 2025
**Nuxt Version**: 4.0.0
