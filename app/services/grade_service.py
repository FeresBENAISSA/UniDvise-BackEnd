from typing import List, Optional
from app.config import Config
from app.models.database import Grade

class GradeService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    async def create_grade(self, student_id: int, course_name: str, grade_value: float, semester: Optional[str] = None) -> Grade:
        data = {
            'student_id': student_id,
            'course_name': course_name,
            'grade_value': grade_value,
            'semester': semester
        }
        result = self.supabase.table('grade').insert(data).execute()
        return result.data[0]

    async def get_grade_by_id(self, grade_id: int) -> Optional[Grade]:
        result = self.supabase.table('grade').select('*').eq('id', grade_id).execute()
        return result.data[0] if result.data else None

    async def get_all_grades(self) -> List[Grade]:
        result = self.supabase.table('grade').select('*').execute()
        return result.data

    async def update_grade(self, grade_id: int, course_name: Optional[str] = None, grade_value: Optional[float] = None, semester: Optional[str] = None) -> Optional[Grade]:
        data = {}
        if course_name:
            data['course_name'] = course_name
        if grade_value:
            data['grade_value'] = grade_value
        if semester:
            data['semester'] = semester

        if not data:
            return None

        result = self.supabase.table('grade').update(data).eq('id', grade_id).execute()
        return result.data[0] if result.data else None

    async def delete_grade(self, grade_id: int) -> bool:
        result = self.supabase.table('grade').delete().eq('id', grade_id).execute()
        return len(result.data) > 0