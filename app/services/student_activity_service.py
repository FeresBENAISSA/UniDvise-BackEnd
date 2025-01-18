from typing import List, Optional
from app.config import Config
from app.models.database import StudentActivity

class StudentActivityService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    async def create_student_activity(self, student_id: int, activity_id: int) -> StudentActivity:
        data = {
            'student_id': student_id,
            'activity_id': activity_id
        }
        result = self.supabase.table('student_activity').insert(data).execute()
        return result.data[0]

    async def get_student_activity_by_id(self, student_id: int, activity_id: int) -> Optional[StudentActivity]:
        result = self.supabase.table('student_activity').select('*').eq('student_id', student_id).eq('activity_id', activity_id).execute()
        return result.data[0] if result.data else None

    async def get_all_student_activities(self) -> List[StudentActivity]:
        result = self.supabase.table('student_activity').select('*').execute()
        return result.data

    async def delete_student_activity(self, student_id: int, activity_id: int) -> bool:
        result = self.supabase.table('student_activity').delete().eq('student_id', student_id).eq('activity_id', activity_id).execute()
        return len(result.data) > 0