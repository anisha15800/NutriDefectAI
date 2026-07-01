import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

import uuid

class MockUser:
    def __init__(self, email):
        self.id = str(uuid.uuid4())
        self.email = email

class MockAuthResponse:
    def __init__(self, email):
        self.user = MockUser(email)
        class Session:
            access_token = "mock-access-token"
        self.session = Session()

class MockAuth:
    def sign_up(self, credentials):
        return MockAuthResponse(credentials.get('email'))
    def sign_in_with_password(self, credentials):
        return MockAuthResponse(credentials.get('email'))

class MockTable:
    def __init__(self, name):
        self.name = name
    def insert(self, data):
        class Executor:
            def execute(self):
                return data
        return Executor()
    def select(self, *args):
        class Filter:
            def eq(self, *args):
                class Executor:
                    def execute(self):
                        class Data:
                            data = []
                        return Data()
                return Executor()
        return Filter()

class MockSupabaseClient:
    def __init__(self):
        self.auth = MockAuth()
        logging.warning("Using MOCK Supabase client because the provided API key was invalid.")
    def table(self, name):
        return MockTable(name)

def get_supabase_client():
    """
    Initializes and returns the Supabase client.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        logging.warning("Supabase URL and Key must be set in .env")
        return MockSupabaseClient()
        
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logging.error(f"Failed to initialize Supabase client: {e}")
        logging.warning("Make sure your API key is a valid JWT (starts with eyJ). Falling back to mock client.")
        return MockSupabaseClient()

supabase = get_supabase_client()
