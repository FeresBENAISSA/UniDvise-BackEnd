from datetime import datetime
from typing import List, Optional
from app.config import Config
from app.models.database import Activity

class ActivityService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    async def create_activity(self, activity_name: str, activity_date: Optional[datetime] = None, description: Optional[str] = None) -> Activity:
        data = {
            'activity_name': activity_name,
            'activity_date': activity_date,
            'description': description
        }
        result = self.supabase.table('activity').insert(data).execute()
        return result.data[0]

    async def get_activity_by_id(self, activity_id: int) -> Optional[Activity]:
        result = self.supabase.table('activity').select('*').eq('id', activity_id).execute()
        return result.data[0] if result.data else None

    async def get_all_activities(self) -> List[Activity]:
        result = self.supabase.table('activity').select('*').execute()
        return result.data

    async def update_activity(self, activity_id: int, activity_name: Optional[str] = None, activity_date: Optional[datetime] = None, description: Optional[str] = None) -> Optional[Activity]:
        data = {}
        if activity_name:
            data['activity_name'] = activity_name
        if activity_date:
            data['activity_date'] = activity_date
        if description:
            data['description'] = description

        if not data:
            return None

        result = self.supabase.table('activity').update(data).eq('id', activity_id).execute()
        return result.data[0] if result.data else None

    async def delete_activity(self, activity_id: int) -> bool:
        result = self.supabase.table('activity').delete().eq('id', activity_id).execute()
        return len(result.data) > 0