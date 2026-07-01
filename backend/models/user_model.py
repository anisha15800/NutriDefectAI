class UserModel:
    """
    A simple class to represent a user in our system.
    This helps standardize data being passed to and from Supabase.
    """
    def __init__(self, user_id, email, full_name=None):
        self.user_id = user_id
        self.email = email
        self.full_name = full_name

    def to_dict(self):
        return {
            "id": self.user_id,
            "email": self.email,
            "full_name": self.full_name
        }

    @staticmethod
    def from_dict(data):
        return UserModel(
            user_id=data.get('id'),
            email=data.get('email'),
            full_name=data.get('full_name')
        )
