class ConsultService:
    @staticmethod
    def get_available_doctors():
        # Mock logic
        return [
            {"id": 1, "name": "Dr. Smith", "specialty": "Dietitian"},
            {"id": 2, "name": "Dr. Doe", "specialty": "Endocrinologist"}
        ]
        
    @staticmethod
    def book_consult(doctor_id, user_id):
        return {"status": "success", "message": f"Booked consultation with doctor {doctor_id}."}
