# Supabase Setup Guide for Krishi Sahayak

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login and create a new project
3. Choose a project name: `krishi-sahayak`
4. Set a strong database password
5. Select region closest to your users (Asia South for India)

## 2. Database Setup

1. Go to SQL Editor in your Supabase dashboard
2. Copy and paste the contents of `supabase_schema.sql`
3. Click "Run" to create all tables and indexes

## 3. Get API Keys

1. Go to Settings > API in your Supabase dashboard
2. Copy the following keys:
   - Project URL
   - Anon (public) key
   - Service role (secret) key

## 4. Environment Configuration

1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_anon_key
   SUPABASE_SERVICE_KEY=your_service_role_key
   ```

## 5. Clerk Authentication Setup

1. Go to [clerk.com](https://clerk.com)
2. Create a new application
3. Get your publishable and secret keys
4. Add to `.env`:
   ```
   CLERK_PUBLISHABLE_KEY=pk_test_...
   CLERK_SECRET_KEY=sk_test_...
   ```

## 6. Install Dependencies

```bash
pip install -r requirements.txt
```

## 7. Test Connection

```python
from config.database import supabase
result = supabase.table('farmers').select('*').limit(1).execute()
print("Connection successful!" if result else "Connection failed!")
```

## Database Schema Overview

### Tables Created:
- **farmers**: User profiles linked to Clerk authentication
- **crops**: Crop details for each farmer
- **insured_crops**: Insurance information for crops
- **nft_certificates**: Blockchain certificates and NFT data
- **plant_scans**: AI disease detection history

### Key Features:
- UUID primary keys for all tables
- Foreign key relationships with CASCADE delete
- Automatic timestamps with triggers
- Indexes for performance optimization
- JSONB fields for flexible data storage