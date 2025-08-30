from config.database import supabase, supabase_admin
from typing import Optional, Dict, List

class Crop:
    def __init__(self, data: Dict):
        self.id = data.get('id')
        self.farmer_id = data.get('farmer_id')
        self.crop_name = data.get('crop_name')
        self.variety = data.get('variety')
        self.area_acres = data.get('area_acres')
        self.planting_date = data.get('planting_date')
        self.expected_harvest_date = data.get('expected_harvest_date')
        self.season = data.get('season')
        self.irrigation_type = data.get('irrigation_type')
        self.farming_method = data.get('farming_method')
        self.status = data.get('status', 'active')

    @classmethod
    def create(cls, crop_data: Dict) -> 'Crop':
        result = supabase_admin.table('crops').insert(crop_data).execute()
        return cls(result.data[0]) if result.data else None

    @classmethod
    def get_by_farmer_id(cls, farmer_id: str) -> List['Crop']:
        result = supabase.table('crops').select('*').eq('farmer_id', farmer_id).execute()
        return [cls(crop) for crop in result.data] if result.data else []

    def update(self, update_data: Dict) -> bool:
        result = supabase_admin.table('crops').update(update_data).eq('id', self.id).execute()
        return bool(result.data)

    def delete(self) -> bool:
        result = supabase_admin.table('crops').delete().eq('id', self.id).execute()
        return bool(result.data)