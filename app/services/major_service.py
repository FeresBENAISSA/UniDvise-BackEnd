from typing import List, Optional
from app.config import Config
from app.models.database import Major

class MajorService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    async def create_major(self, name: str, university_id: Optional[int] = None) -> Major:
        """Create a new major."""
        data = {
            'name': name,
            'university_id': university_id
        }
        result = self.supabase.table('major').insert(data).execute()
        return result.data[0]

    async def get_major_by_id(self, major_id: int) -> Optional[Major]:
        """Fetch a major by its ID."""
        result = self.supabase.table('major').select('*').eq('id', major_id).execute()
        return result.data[0] if result.data else None

    async def get_all_majors(self) -> List[Major]:
        """Fetch all majors."""
        result = self.supabase.table('major').select('*').execute()
        return result.data

    async def update_major(self, major_id: int, name: Optional[str] = None, university_id: Optional[int] = None) -> Optional[Major]:
        """Update an existing major."""
        data = {}
        if name:
            data['name'] = name
        if university_id:
            data['university_id'] = university_id

        if not data:
            return None  # No fields to update

        result = self.supabase.table('major').update(data).eq('id', major_id).execute()
        return result.data[0] if result.data else None

    async def delete_major(self, major_id: int) -> bool:
        """Delete a major by its ID."""
        result = self.supabase.table('major').delete().eq('id', major_id).execute()
        return len(result.data) > 0

    async def assign_major_to_university(self, major_id: int, university_id: int) -> Optional[Major]:
        """Assign a major to a university by updating its university_id."""
        try:
            # Check if the major exists
            major_result = self.supabase.table('major').select('*').eq('id', major_id).execute()
            if not major_result.data:
                return None  # Major not found

            # Update the major's university_id
            update_result = self.supabase.table('major').update({'university_id': university_id}).eq('id', major_id).execute()
            if update_result.data:
                return update_result.data[0]  # Return the updated major
            else:
                return None  # Update failed
        except Exception as e:
            print(f"Error assigning major to university: {e}")
            return None