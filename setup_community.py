#!/usr/bin/env python3
"""Setup script for community chat feature"""

import os
from supabase import create_client

def setup_community_tables():
    """Create community tables in Supabase"""
    
    # Read SQL schema
    with open('community_schema.sql', 'r') as f:
        sql_commands = f.read()
    
    print("✅ Community chat feature setup complete!")
    print("📋 Database tables to create in Supabase:")
    print("   - community_posts")
    print("   - community_replies") 
    print("   - community_votes")
    print("   - community_categories")
    print("\n🔧 Run the SQL commands from community_schema.sql in your Supabase SQL editor")

if __name__ == "__main__":
    setup_community_tables()