import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not all([self.url, self.anon_key]):
            raise ValueError("Missing Supabase configuration")
    
    def get_client(self, use_service_key=False):
        key = self.service_key if use_service_key else self.anon_key
        return create_client(self.url, key)

# Global Supabase client
supabase_config = SupabaseConfig()
supabase: Client = supabase_config.get_client()
supabase_admin: Client = supabase_config.get_client(use_service_key=True)