from config.database import supabase, supabase_admin
from typing import Optional, Dict, List
from datetime import datetime
import dateutil.parser

class DigitalPassport:
    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.farmer_id = data.get('farmer_id')
        self.crop_type = data.get('crop_type')
        self.season = data.get('season')
        self.nft_token_id = data.get('nft_token_id')
        self.ipfs_hash = data.get('ipfs_hash')
        created_at_str = data.get('created_at')
        if isinstance(created_at_str, str):
            try:
                self.created_at = dateutil.parser.parse(created_at_str)
            except:
                self.created_at = created_at_str
        else:
            self.created_at = created_at_str
        self.verified = data.get('verified', False)

    @classmethod
    def create(cls, passport_data: Dict) -> 'DigitalPassport':
        try:
            print(f"DEBUG: Creating passport with data: {passport_data}")
            result = supabase_admin.table('digital_passports').insert(passport_data).execute()
            print(f"DEBUG: Supabase insert result: {result}")
            if result.data:
                print(f"DEBUG: Passport created with ID: {result.data[0].get('id')}")
                return cls(result.data[0])
            else:
                print("DEBUG: No data returned from Supabase insert")
                return None
        except Exception as e:
            print(f"DEBUG: Supabase create error: {e}")
            return None

    @classmethod
    def get_by_farmer_id(cls, farmer_id: str) -> List['DigitalPassport']:
        try:
            print(f"DEBUG: Querying passports for farmer_id: {farmer_id}")
            result = supabase.table('digital_passports').select('*').eq('farmer_id', farmer_id).order('created_at', desc=True).execute()
            print(f"DEBUG: Supabase query result: {result}")
            if result.data:
                print(f"DEBUG: Found {len(result.data)} passports in database")
                for p in result.data:
                    print(f"  - DB Record: {p.get('crop_type')} {p.get('season')} (ID: {p.get('id')})")
            else:
                print("DEBUG: No passports found in database")
            return [cls(passport) for passport in result.data] if result.data else []
        except Exception as e:
            print(f"DEBUG: Supabase query error: {e}")
            return []

    @classmethod
    def get_by_token_id(cls, token_id: str) -> Optional['DigitalPassport']:
        try:
            result = supabase.table('digital_passports').select('*').eq('nft_token_id', token_id).execute()
            return cls(result.data[0]) if result.data else None
        except:
            return None