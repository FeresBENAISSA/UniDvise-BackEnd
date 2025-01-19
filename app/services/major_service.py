from typing import List, Optional

from flask import abort

from app.models.database import Major, UniversityMajor
from app.config import Config

class MajorService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    def create_major(self, name: str) -> Optional[Major]:
        """Create a new major."""
        data = {'name': name}
        result = self.supabase.table('majors').insert(data).execute()
        return result.data[0] if result.data else None

    def get_major_by_id(self, major_id: int) -> Optional[Major]:
        """Fetch a major by its ID."""
        result = self.supabase.table('majors').select('*').eq('major_id', major_id).execute()
        return result.data[0] if result.data else None

    def get_all_majors(self) -> List[Major]:
        """Fetch all majors."""
        result = self.supabase.table('majors').select('*').execute()
        return result.data

    def update_major(self, major_id: int, name: Optional[str] = None) -> Optional[Major]:
        """Update an existing major."""
        data = {}
        if name:
            data['name'] = name

        if not data:
            return None  # No fields to update

        result = self.supabase.table('majors').update(data).eq('major_id', major_id).execute()
        return result.data[0] if result.data else None

    def delete_major(self, major_id: int) -> bool:
        """Delete a major by its ID."""
        result = self.supabase.table('majors').delete().eq('major_id', major_id).execute()
        return len(result.data) > 0

    def assign_major_to_university(self, major_id: int, university_id: int, max_capacity: int, minimum_score: int) -> Optional[UniversityMajor]:
        """Assign a major to a university by creating a UniversityMajor record."""
        try:
            # Check if the major and university exist
            major_result = self.supabase.table('majors').select('*').eq('major_id', major_id).execute()
            university_result = self.supabase.table('universities').select('*').eq('university_id', university_id).execute()

            if not major_result.data or not university_result.data:
                return None  # Major or University not found

            # Check if the university-major combination already exists
            existing_combination = self.supabase.table('university_major') \
                .select('*') \
                .eq('university_id', university_id) \
                .eq('major_id', major_id) \
                .execute()

            if existing_combination.data:
                print("Error: This university-major combination already exists.")
                abort(500, description="Error: This university-major combination already exists.")
                return None  # Combination already exists

            # Create a UniversityMajor record
            data = {
                'university_id': university_id,
                'major_id': major_id,
                'maxcapacity': max_capacity,
                'minimumscore': minimum_score
            }
            result = self.supabase.table('university_major').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error assigning major to university: {e}")
            return None