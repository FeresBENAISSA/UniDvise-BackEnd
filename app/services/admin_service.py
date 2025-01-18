from typing import List, Optional
from app.config import Config
from app.models.database import Admin

class AdminService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    async def create_admin(self, username: str, password_hash: str, email: str) -> Admin:
        data = {
            'username': username,
            'password_hash': password_hash,
            'email': email
        }
        result = self.supabase.table('admin').insert(data).execute()
        return result.data[0]

    async def get_admin_by_id(self, admin_id: int) -> Optional[Admin]:
        result = self.supabase.table('admin').select('*').eq('id', admin_id).execute()
        return result.data[0] if result.data else None

    async def get_all_admins(self) -> List[Admin]:
        result = self.supabase.table('admin').select('*').execute()
        return result.data

    async def update_admin(self, admin_id: int, username: Optional[str] = None, email: Optional[str] = None) -> Optional[Admin]:
        data = {}
        if username:
            data['username'] = username
        if email:
            data['email'] = email

        if not data:
            return None

        result = self.supabase.table('admin').update(data).eq('id', admin_id).execute()
        return result.data[0] if result.data else None

    async def delete_admin(self, admin_id: int) -> bool:
        result = self.supabase.table('admin').delete().eq('id', admin_id).execute()
        return len(result.data) > 0