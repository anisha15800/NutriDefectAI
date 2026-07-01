import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class DietService:
    @staticmethod
    def generate_goal_based_diet(user_data):
        if not GEMINI_API_KEY:
            return {
                "error": "Gemini API Key missing. Cannot generate AI diet."
            }

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Act as an expert fitness and nutrition coach.
            A user wants a 7-day diet plan tailored to their specific fitness goal.
            
            User Profile:
            Age: {user_data.get('age')}
            Gender: {user_data.get('gender')}
            Height: {user_data.get('height')} cm
            Weight: {user_data.get('weight')} kg
            Diet Preference: {user_data.get('diet_preference')}
            Lifestyle: {user_data.get('lifestyle')}
            Primary Goal: {user_data.get('goal')}
            
            First, calculate an estimated daily calorie target based on their profile and goal.
            
            Then, provide a JSON response with exactly these keys:
            "guidance": string (A 2-3 sentence expert introductory guidance on how they should approach their goal, mentioning their estimated calorie target),
            "diet_plan": string (A complete 7-day diet plan formatted as clean HTML. Use <h4> for days (Monday to Sunday) and bullet points <ul><li> for Breakfast, Lunch, and Dinner. Ensure the meals strictly follow their '{user_data.get('diet_preference')}' preference and align with their goal.)
            
            Ensure the output is ONLY raw, valid JSON without any markdown blocks like ```json.
            """
            
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()
                
            result = json.loads(text)
            return result
        except Exception as e:
            logging.error(f"Gemini AI goal diet generation failed: {e}")
            return {"error": str(e)}

    @staticmethod
    def get_recommendations(user_id):
        # Existing mock logic
        return {
            "status": "success",
            "recommendations": [
                "Increase protein intake by 15%",
                "Drink 2 more liters of water daily",
                "Add leafy greens to dinner"
            ]
        }
