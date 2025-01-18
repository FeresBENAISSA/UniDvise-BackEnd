from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

class Config:
    # Access environment variables
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    @staticmethod
    def init_supabase() -> Client:
        return create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)