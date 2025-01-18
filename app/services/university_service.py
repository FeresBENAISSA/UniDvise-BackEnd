from typing import List, Optional
from datetime import datetime

from aiohttp import ClientError
from supabase import Client, create_client
from app.config import Config
from app.models.database import University, Student, Major, Admin, Grade, Activity, StudentActivity
# from supabase.lib.client_options import ClientError

class UniversityService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    def get_all_universities(self) -> List[University]:
        """Fetch all universities from the database."""
        try:
            result = self.supabase.table('university').select('*').execute()
            return [University(**university) for university in result.data]
        except ClientError as e:
            print(f"Error fetching universities: {e}")
            return []

    def get_university_by_id(self, university_id: int) -> Optional[University]:
        """Fetch a university by its ID."""
        try:
            result = self.supabase.table('university').select('*').eq('id', university_id).execute()
            return University(**result.data[0]) if result.data else None
        except ClientError as e:
            print(f"Error fetching university with ID {university_id}: {e}")
            return None

    def create_university(self, name: str, location: Optional[str] = None, minscore: Optional[str] = None, admin_id: Optional[int] = None) -> Optional[University]:
        """Create a new university."""
        try:
            data = {
                'name': name,
                'location': location,
                'minscore': minscore,
                'admin_id': admin_id,
            }
            result = self.supabase.table('university').insert(data).execute()
            return University(**result.data[0])
        except ClientError as e:
            print(f"Error creating university: {e}")
            return None

    def update_university(self, university_id: int, name: Optional[str] = None, location: Optional[str] = None, admin_id: Optional[int] = None) -> Optional[University]:
        """Update an existing university."""
        try:
            data = {}
            if name:
                data['name'] = name
            if location:
                data['location'] = location
            if admin_id:
                data['admin_id'] = admin_id

            if not data:
                return None

            result = self.supabase.table('university').update(data).eq('id', university_id).execute()
            return University(**result.data[0]) if result.data else None
        except ClientError as e:
            print(f"Error updating university with ID {university_id}: {e}")
            return None

    def delete_university(self, university_id: int) -> bool:
        """Delete a university by its ID."""
        try:
            result = self.supabase.table('university').delete().eq('id', university_id).execute()
            return len(result.data) > 0
        except ClientError as e:
            print(f"Error deleting university with ID {university_id}: {e}")
            return False

    def get_university_students(self, university_id: int) -> List[Student]:
        """Fetch all students belonging to a specific university."""
        try:
            result = self.supabase.table('student').select('*').eq('university_id', university_id).execute()
            return [Student(**student) for student in result.data]
        except ClientError as e:
            print(f"Error fetching students for university with ID {university_id}: {e}")
            return []

    def get_university_majors(self, university_id: int) -> List[Major]:
        """Fetch all majors offered by a specific university."""
        try:
            result = self.supabase.table('major').select('*').eq('university_id', university_id).execute()
            return [Major(**major) for major in result.data]
        except ClientError as e:
            print(f"Error fetching majors for university with ID {university_id}: {e}")
            return []

    def get_university_activities(self, university_id: int) -> List[Activity]:
        """Fetch all activities associated with a specific university."""
        try:
            result = self.supabase.table('activity').select('*').eq('university_id', university_id).execute()
            return [Activity(**activity) for activity in result.data]
        except ClientError as e:
            print(f"Error fetching activities for university with ID {university_id}: {e}")
            return []

    def get_university_grades(self, university_id: int) -> List[Grade]:
        """Fetch all grades for students belonging to a specific university."""
        try:
            students = self.get_university_students(university_id)
            if not students:
                return []

            student_ids = [student.id for student in students]
            result = self.supabase.table('grade').select('*').in_('student_id', student_ids).execute()
            return [Grade(**grade) for grade in result.data]
        except ClientError as e:
            print(f"Error fetching grades for university with ID {university_id}: {e}")
            return []

