# 🔐 Krishi Sahayak Authentication Flow

## Overview
The authentication system now enforces proper Clerk authentication before allowing access to any features.

## Authentication Flow

### 1. Landing Page (`/`)
- **Unauthenticated users**: See landing page with "Get Started" button
- **Authenticated users with profile**: Redirect to `/dashboard`
- **Authenticated users without profile**: Redirect to `/profile`

### 2. Login Process (`/login`)
- Shows Clerk authentication component
- Users must sign in with Google via Clerk
- No demo mode or bypass options available
- On successful authentication:
  - If user has existing profile → Redirect to `/dashboard`
  - If new user → Redirect to `/profile`

### 3. Profile Setup (`/profile`)
- **Access**: Requires `clerk_user_id` in session
- **Purpose**: Collect farming information and create Supabase profile
- **Required fields**:
  - Full Name
  - Village/City
  - PIN Code (6 digits)
  - Main Crops (optional but recommended)
- **Validation**:
  - All required fields must be filled
  - PIN code must be exactly 6 digits
  - Form data is validated before submission
- **On success**: Creates farmer profile in Supabase and redirects to `/dashboard`

### 4. Protected Routes
All farming features require both:
1. **Clerk Authentication**: `clerk_user_id` in session
2. **Profile Completion**: `user_id` in session (Supabase farmer ID)

Protected routes:
- `/dashboard` - Main farming dashboard
- `/scanner` - AI plant disease detection
- `/weather` - Weather forecasting
- `/market` - Market prices
- `/passport` - Digital crop certificates
- `/results` - Scan results

### 5. Session Management
- **Clerk Session**: Stores `clerk_user_id`, `clerk_email`, `clerk_phone`
- **App Session**: Stores `user_id` (Supabase farmer ID)
- **Logout**: Clears all session data

## Security Features

### 1. No Bypass Options
- Removed all demo mode fallbacks
- No direct access to protected routes
- Proper error messages guide users to authentication

### 2. Validation
- Server-side validation for all form inputs
- PIN code format validation
- Required field validation
- Proper error handling and user feedback

### 3. Database Integration
- Supabase for secure data storage
- Proper user lookup by Clerk ID
- Error handling for database operations

## Environment Variables Required

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# Clerk Authentication
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key

# Other APIs
GROQ_API_KEY=your_groq_api_key
ACCUWEATHER_API_KEY=your_accuweather_api_key
GEMINI_API_KEY=your_gemini_api_key
SESSION_SECRET=your_session_secret_key
```

## Testing the Flow

Run the test script to verify everything is working:

```bash
python3 test_auth_flow.py
```

## User Experience

### New User Journey
1. Visit app → See landing page
2. Click "Get Started" → Redirected to Clerk login
3. Sign in with Google → Account created in Clerk
4. Redirected to profile setup → Fill farming details
5. Profile saved → Redirected to dashboard
6. Full access to all farming features

### Returning User Journey
1. Visit app → Automatic Clerk authentication check
2. If authenticated → Direct to dashboard
3. If not authenticated → Redirected to login
4. Sign in → Direct to dashboard

## Error Handling

### Authentication Errors
- Missing Clerk session → "Please sign in with Google first"
- Missing profile → "Please complete your profile setup"
- Invalid form data → Specific validation messages

### Database Errors
- Supabase connection issues → Graceful error handling
- Profile creation failures → User-friendly error messages
- Data retrieval errors → Fallback to safe defaults

## Benefits

1. **Security**: No unauthorized access to farming data
2. **User Experience**: Clear flow with helpful messages
3. **Data Integrity**: Proper validation and error handling
4. **Scalability**: Proper separation of authentication and application logic
5. **Compliance**: Secure handling of user data with Clerk + Supabase