from config.supabase_config import supabase
from utils.token_utils import generate_token

class AuthService:
    @staticmethod
    def sign_up(email, password, full_name):
        """
        Registers a new user with Supabase.
        """
        try:
            # Create user in Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if not auth_response.user:
                return {"error": "Failed to create user"}, 400

            # Create profile in our custom public.users table
            user_id = auth_response.user.id
            profile_data = {
                "id": user_id,
                "email": email,
                "full_name": full_name
            }
            supabase.table("users").insert(profile_data).execute()

            # Generate token so user is instantly logged in
            token = generate_token(user_id, email)

            return {
                "message": "User created successfully", 
                "token": token,
                "user": profile_data
            }, 201
            
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def sign_in(email, password):
        """
        Authenticates a user with Supabase.
        """
        try:
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not auth_response.user:
                return {"error": "Invalid credentials"}, 401

            # Fetch user profile
            user_id = auth_response.user.id
            profile = supabase.table("users").select("*").eq("id", user_id).execute()
            
            user_data = profile.data[0] if profile.data else {"email": email}

            # Generate our own custom JWT token (optional, Supabase also provides one)
            token = generate_token(user_id, email)

            return {
                "message": "Sign in successful",
                "token": token,
                "supabase_token": auth_response.session.access_token,
                "user": user_data
            }, 200
            
        except Exception as e:
            return {"error": str(e)}, 401
