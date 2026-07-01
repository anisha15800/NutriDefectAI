import os
import sys
import uuid
import logging
import json
import google.generativeai as genai
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.config.supabase_config import get_supabase_client

load_dotenv()
supabase = get_supabase_client()

# Configure Gemini if key is present
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AssessmentService:
    @staticmethod
    def suggest_symptoms(current_symptoms):
        """
        Uses Gemini AI to suggest similar or related symptoms based on user inputs.
        Falls back to heuristics if API key is not configured or if API fails.
        """
        current = [s.lower().strip() for s in current_symptoms]
        
        # Try using Gemini AI
        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""
                A patient has reported the following symptoms: {', '.join(current)}.
                Based on these symptoms, what are 5 other related or underlying symptoms they might also be experiencing?
                Return ONLY a valid JSON array of strings containing the 5 symptom names.
                """
                response = model.generate_content(prompt)
                
                # Try to parse the response text as JSON
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text.replace("```json", "").replace("```", "").strip()
                elif text.startswith("```"):
                    text = text.replace("```", "").strip()
                    
                suggestions = json.loads(text)
                
                # Filter out already existing symptoms
                final_suggestions = [s.strip() for s in suggestions if s.lower().strip() not in current]
                if final_suggestions:
                    return final_suggestions[:5]
            except Exception as e:
                logging.error(f"Gemini AI suggestion failed: {e}")
                # Fallback to heuristic below if it fails
                pass

        # Heuristic Fallback
        suggestions = []
        if "fatigue" in current or "weakness" in current:
            suggestions.extend(["Pale skin", "Cold hands and feet", "Shortness of breath"])
        if "hair loss" in current or "brittle nails" in current:
            suggestions.extend(["Dry skin", "Muscle weakness", "Low mood"])
        if "bone pain" in current or "muscle cramps" in current:
            suggestions.extend(["Joint stiffness", "Fatigue", "Frequent illness"])
            
        unique_suggestions = list(set(suggestions))
        final_suggestions = [s for s in unique_suggestions if s.lower() not in current]
        
        if not final_suggestions:
            final_suggestions = ["Fatigue", "Headache", "Dizziness", "Poor sleep"]
            
        return final_suggestions[:5]

    @staticmethod
    def generate_followup_questions(user_data):
        """
        Uses Gemini AI to generate follow-up questions based on initial symptoms.
        Returns a list of dictionaries with 'question' and 'options'.
        """
        symptoms = [s.lower().strip() for s in user_data.get('symptoms', [])]
        history = user_data.get('medical_history', '').lower()
        age = user_data.get('age')
        gender = user_data.get('gender')
        
        # Try using Gemini AI
        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""
                Act as a medical AI diagnostic assistant. Analyze this patient profile:
                Age: {age}, Gender: {gender}
                Medical History: {history}
                Initial Symptoms: {', '.join(symptoms)}
                
                Generate exactly 3 follow-up multiple-choice questions to narrow down the potential nutritional deficiency or underlying cause.
                Each question should have 3 to 4 distinct options.
                
                Return ONLY a valid JSON array of objects. Format:
                [
                  {{"question": "How long have you had the fatigue?", "options": ["Less than a week", "1-4 weeks", "More than a month"]}},
                  ...
                ]
                """
                response = model.generate_content(prompt)
                
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text.replace("```json", "").replace("```", "").strip()
                elif text.startswith("```"):
                    text = text.replace("```", "").strip()
                    
                questions = json.loads(text)
                if isinstance(questions, list) and len(questions) > 0:
                    return questions
            except Exception as e:
                logging.error(f"Gemini AI followup generation failed: {e}")
                pass

        # Heuristic Fallback
        return [
            {
                "question": "Are your symptoms worse at a specific time of day?",
                "options": ["Morning", "Evening", "Constant throughout the day", "Randomly"]
            },
            {
                "question": "How would you describe your overall energy levels lately?",
                "options": ["Normal", "Slightly drained", "Completely exhausted"]
            },
            {
                "question": "Have you noticed any recent changes in your sleep or appetite?",
                "options": ["Sleeping less/Eating less", "Sleeping more/Eating more", "No significant changes"]
            }
        ]

    @staticmethod
    def generate_final_report(user_data, user_email=None):
        """
        Uses Gemini AI to generate a comprehensive health report.
        Falls back to heuristic mapping.
        """
        symptoms = [s.lower().strip() for s in user_data.get('symptoms', [])]
        followup_answers = user_data.get('followup_answers', [])
        history = user_data.get('medical_history', '').lower()
        age = user_data.get('age')
        gender = user_data.get('gender')
        bmi = user_data.get('bmi')

        result = None
        
        # Try using Gemini AI
        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                followup_text = ""
                if followup_answers:
                    followup_text = "Follow-up Answers:\n" + "\n".join([f"Q: {qa['question']} A: {qa['answer']}" for qa in followup_answers])
                
                prompt = f"""
                Act as a medical AI assistant. Analyze this patient profile:
                Age: {age}, Gender: {gender}, BMI: {bmi}
                Diet Preference: {user_data.get('diet_preference', 'Not specified')}
                Lifestyle: {user_data.get('lifestyle', 'Not specified')}
                Medical History: {history}
                Current Symptoms: {', '.join(symptoms)}
                {followup_text}
                
                Provide a JSON response with exactly these keys:
                "deficiency": string (The most likely nutritional deficiency),
                "diet_recommendations": list of strings (4-5 foods/dietary changes to help),
                "recommended_tests": list of strings (2-3 blood tests to confirm),
                "recommended_doctors": list of strings (1-2 specialist doctor types)
                
                Ensure the output is ONLY raw, valid JSON.
                """
                response = model.generate_content(prompt)
                
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text.replace("```json", "").replace("```", "").strip()
                elif text.startswith("```"):
                    text = text.replace("```", "").strip()
                    
                result = json.loads(text)
            except Exception as e:
                logging.error(f"Gemini AI report generation failed: {e}")
                pass

        # Heuristic Fallback
        if not result:
            deficiency = "General Nutritional Imbalance"
            diet = ["Balanced Plate", "Increase Hydration", "Multivitamin"]
            tests = ["Complete Blood Count (CBC)"]
            doctors = ["General Physician", "Nutritionist"]
            
            if "fatigue" in symptoms or "pale" in symptoms or "anemia" in history:
                deficiency = "Iron Deficiency (Anemia Risk)"
                diet = ["Spinach", "Red Meat", "Lentils", "Vitamin C (for absorption)"]
                tests = ["Serum Ferritin", "Hemoglobin Levels"]
                doctors = ["Hematologist", "Dietitian"]
            elif "bone pain" in symptoms or "muscle cramps" in symptoms:
                deficiency = "Vitamin D / Calcium Deficiency"
                diet = ["Fortified Milk", "Fatty Fish", "Eggs", "Sunlight exposure"]
                tests = ["25-OH Vitamin D Test", "Calcium Blood Test"]
                doctors = ["Endocrinologist", "Orthopedic"]
            elif "hair loss" in symptoms or "brittle nails" in symptoms:
                deficiency = "Biotin / Zinc Deficiency"
                diet = ["Nuts and Seeds", "Eggs", "Whole Grains"]
                tests = ["Zinc Levels", "B-Complex Panel"]
                doctors = ["Dermatologist", "Nutritionist"]

            result = {
                "deficiency": deficiency,
                "diet_recommendations": diet,
                "recommended_tests": tests,
                "recommended_doctors": doctors
            }

        # Save to database
        try:
            record = {
                "id": str(uuid.uuid4()),
                "user_email": user_email or "anonymous",
                "age": age,
                "gender": gender,
                "bmi": bmi,
                "medical_history": user_data.get('medical_history'),
                "symptoms": user_data.get('symptoms'),
                "prediction_result": result
            }
            supabase.table('assessments').insert(record).execute()
        except Exception as e:
            logging.error(f"Failed to save assessment to database: {e}")

        return result

    @staticmethod
    def generate_diet_plan(deficiency, user_data):
        """
        Uses Gemini AI to generate a 7-day diet plan to overcome the deficiency.
        Falls back to a generic diet plan if API key is missing or fails.
        """
        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""
                Act as an expert nutritionist. The patient has been predicted to have the following deficiency/issue: {deficiency}.
                Their profile: Age {user_data.get('age')}, Gender {user_data.get('gender')}, BMI {user_data.get('bmi')}.
                Diet Preference: {user_data.get('diet_preference', 'Not specified')}.
                Lifestyle: {user_data.get('lifestyle', 'Not specified')}.
                
                Please generate a complete 7-day diet plan (Monday to Sunday) outlining Breakfast, Lunch, and Dinner.
                Focus heavily on meals that will help overcome their specific deficiency while STRICTLY adhering to their {user_data.get('diet_preference', 'Diet Preference')}.
                
                Format the response as clear HTML. Use <h4> for days, and bullet points for meals. Do not use markdown wrappers like ```html.
                """
                response = model.generate_content(prompt)
                
                text = response.text.strip()
                if text.startswith("```html"):
                    text = text.replace("```html", "").replace("```", "").strip()
                elif text.startswith("```"):
                    text = text.replace("```", "").strip()
                    
                return text
            except Exception as e:
                logging.error(f"Gemini AI diet generation failed: {e}")
                pass

        # Heuristic Fallback
        return f"""
        <h4>Monday to Sunday Generic Plan for {deficiency}</h4>
        <ul>
            <li><strong>Breakfast:</strong> Oatmeal with mixed nuts and berries, or fortified cereal.</li>
            <li><strong>Lunch:</strong> Large leafy green salad with grilled chicken or chickpeas, and olive oil dressing.</li>
            <li><strong>Dinner:</strong> Baked salmon or tofu with steamed broccoli and quinoa.</li>
        </ul>
        """
