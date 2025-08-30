"""
Debug database connection and farmer records
"""

import os
from dotenv import load_dotenv
load_dotenv()

def debug_database():
    try:
        from supabase_models.farmer import Farmer
        from config.database import supabase
        
        print("🔍 Database Debug")
        print("=" * 40)
        
        # Test connection
        result = supabase.table('farmers').select('count').execute()
        print(f"✅ Database connected")
        
        # List all farmers
        farmers = supabase.table('farmers').select('*').execute()
        print(f"📊 Total farmers: {len(farmers.data)}")
        
        for farmer in farmers.data:
            print(f"  - ID: {farmer.get('id')}")
            print(f"    Clerk ID: {farmer.get('clerk_user_id')}")
            print(f"    Name: {farmer.get('name')}")
            print(f"    Email: {farmer.get('email')}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    debug_database()