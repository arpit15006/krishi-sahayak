from config.database import supabase, supabase_admin
from typing import Optional, Dict, List

class Farmer:
    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.clerk_user_id = data.get('clerk_user_id')
        self.name = data.get('name')
        self.phone = data.get('phone')
        self.email = data.get('email')
        self.place = data.get('place')
        self.district = data.get('district')
        self.state = data.get('state')
        self.pincode = data.get('pincode')
        self.farm_size_acres = data.get('farm_size_acres')
        self.farming_experience_years = data.get('farming_experience_years')
        self.preferred_language = data.get('preferred_language', 'en')

    @classmethod
    def create(cls, farmer_data: Dict) -> 'Farmer':
        try:
            # Check if farmer already exists
            existing = cls.get_by_clerk_id(farmer_data.get('clerk_user_id'))
            if existing:
                print(f"Farmer already exists: {farmer_data.get('clerk_user_id')}")
                return existing
            
            result = supabase_admin.table('farmers').insert(farmer_data).execute()
            if result.data:
                return cls(result.data[0])
            else:
                print(f"No data returned from insert: {result}")
                return None
        except Exception as e:
            print(f"Database error in create: {e}")
            raise e

    @classmethod
    def get_by_clerk_id(cls, clerk_user_id: str) -> Optional['Farmer']:
        result = supabase.table('farmers').select('*').eq('clerk_user_id', clerk_user_id).execute()
        return cls(result.data[0]) if result.data else None

    @classmethod
    def get_by_phone(cls, phone: str) -> Optional['Farmer']:
        result = supabase.table('farmers').select('*').eq('phone', phone).execute()
        return cls(result.data[0]) if result.data else None

    @classmethod
    def get_by_id(cls, farmer_id: str) -> Optional['Farmer']:
        result = supabase.table('farmers').select('*').eq('id', farmer_id).execute()
        return cls(result.data[0]) if result.data else None

    def update(self, update_data: Dict) -> bool:
        result = supabase_admin.table('farmers').update(update_data).eq('id', self.id).execute()
        return bool(result.data)

    def get_crops(self) -> List[Dict]:
        result = supabase.table('crops').select('*').eq('farmer_id', self.id).execute()
        return result.data or []