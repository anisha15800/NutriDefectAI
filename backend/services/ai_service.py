import os
import json
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AIService:
    @staticmethod
    def process_voice_consult(transcript):
        if not GEMINI_API_KEY:
            return {"error": "Gemini API Key missing. Cannot process voice consult."}

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Act as a friendly, empathetic, and professional medical AI voice assistant for a nutrition and health platform.
            A user has spoken the following to you via voice input:
            "{transcript}"
            
            Respond directly to the user as if you are speaking to them.
            Keep your response concise, conversational, and easy to listen to (maximum 3-4 short sentences).
            Do not use markdown formatting like asterisks or bullet points, as this will be read aloud by a Text-to-Speech engine.
            Offer immediate, brief advice based on their symptoms, and recommend they use the platform's diagnostic tools if necessary.
            """
            
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            return {"response": text}
        except Exception as e:
            logging.error(f"Gemini AI voice consult failed: {e}")
            return {"error": str(e)}

    @staticmethod
    def analyze_food_image(base64_image, portion_size):
        if not GEMINI_API_KEY:
            return {"error": "Gemini API Key missing."}

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Prepare image part for Gemini
            image_part = {
                "mime_type": "image/jpeg",
                "data": base64_image
            }

            portion_context = ""
            if portion_size and portion_size.strip() != "":
                portion_context = f"The user has specified the portion size as: '{portion_size}'. Base your macro calculations strictly on this specific portion size instead of guessing visually."
            else:
                portion_context = "Estimate the portion size visually from the image to calculate the macros."

            prompt = f"""
            Act as an expert nutritionist AI. Analyze the provided image of food.
            {portion_context}
            
            Respond ONLY with a valid JSON object containing exactly these keys:
            "food_name": string (A short, descriptive name of the meal/food),
            "health_rating": string (A score out of 10, e.g. "7.5"),
            "calories": integer (Total estimated calories),
            "macros": object with keys "protein", "carbs", "fats" (all integers representing grams),
            "micros": list of strings (List 2-4 notable vitamins/minerals present in the food),
            "summary": string (A 2-3 sentence verdict explaining the health rating and nutritional impact)
            
            Do not include markdown blocks like ```json. Return raw JSON only.
            """
            
            response = model.generate_content([prompt, image_part])
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()
                
            result = json.loads(text)
            return result
        except Exception as e:
            logging.error(f"Gemini AI food analysis failed: {e}")
            return {"error": str(e)}

    @staticmethod
    def analyze_face_image(base64_image):
        if not GEMINI_API_KEY:
            return {"error": "Gemini API Key missing."}

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Prepare image part for Gemini
            image_part = {
                "mime_type": "image/jpeg",
                "data": base64_image
            }

            prompt = """
            Act as an expert clinical diagnostician. Analyze the provided image of a patient's face or body part.
            Specifically scan for visible signs of nutritional deficiencies or related medical symptoms (e.g., pale skin, dry eyes, brittle hair, cracked lips, etc.).
            
            Respond ONLY with a valid JSON object containing exactly these keys:
            "detected_symptoms": list of strings (e.g., ["Pale conjunctiva", "Angular cheilitis"]),
            "potential_deficiencies": list of objects, each with "name" (string, e.g., "Iron Deficiency") and "reason" (string, brief explanation of why),
            "summary": string (A detailed 3-4 sentence clinical summary of what you found and what it might indicate)
            
            If you do not detect any obvious symptoms, state that in the summary.
            Do not include markdown blocks like ```json. Return raw JSON only.
            """
            
            response = model.generate_content([prompt, image_part])
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()
                
            result = json.loads(text)
            return result
        except Exception as e:
            logging.error(f"Gemini AI face analysis failed: {e}")
            return {"error": str(e)}

    @staticmethod
    def analyze_blood_report(base64_image):
        if not GEMINI_API_KEY:
            return {"error": "Gemini API Key missing."}

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Prepare image part for Gemini
            image_part = {
                "mime_type": "image/jpeg",
                "data": base64_image
            }

            prompt = """
            Act as an expert clinical nutritionist and OCR engine. Analyze the provided image of a blood test / medical lab report.
            Extract the biomarker data and specifically identify any values that fall outside of the normal/healthy reference ranges provided in the report.
            
            Based ONLY on the abnormal values, suggest specific dietary changes (foods to eat or avoid) to help bring those markers back into range.
            
            Respond ONLY with a valid JSON object containing exactly these keys:
            "abnormalities": list of objects, each with "marker" (string, e.g., "Hemoglobin") and "issue" (string, e.g., "Low (10.5 g/dL)"),
            "dietary_recommendations": list of strings (e.g., ["Increase intake of iron-rich foods like spinach and red meat."]),
            "summary": string (A detailed 3-4 sentence summary of the report's nutritional implications)
            
            If you do not detect any abnormal values or cannot read the report clearly, state that in the summary and leave the lists empty.
            Do not include markdown blocks like ```json. Return raw JSON only.
            """
            
            response = model.generate_content([prompt, image_part])
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()
                
            result = json.loads(text)
            return result
        except Exception as e:
            logging.error(f"Gemini AI blood report analysis failed: {e}")
            return {"error": str(e)}

    @staticmethod
    def find_doctors(city, locality, specialist):
        if not GEMINI_API_KEY:
            return {"error": "Gemini API Key missing."}

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Act as a directory service for medical specialists. The user is looking for a {specialist} in {locality}, {city}.
            Generate 3 to 4 highly realistic (but simulated) doctor profiles matching these criteria.
            
            Respond ONLY with a valid JSON object containing exactly this key:
            "doctors": list of objects, each with:
              - "name" (string, e.g., "Dr. Sarah Jenkins")
              - "specialty" (string, e.g., "Clinical Dietitian")
              - "qualifications" (string, e.g., "MBBS, MD - Nutrition")
              - "experience" (integer, e.g., 12)
              - "clinic_name" (string, e.g., "HealthFirst Clinic")
              - "address" (string, realistic street address in {locality}, {city})
              - "phone" (string, e.g., "+1 (555) 019-2834")
              - "email" (string, e.g., "dr.jenkins@healthfirst.com")
            
            Do not include markdown blocks like ```json. Return raw JSON only.
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
            logging.error(f"Gemini AI doctor search failed: {e}")
            return {"error": str(e)}

    @staticmethod
    def process_concerns(concerns):
        # Existing mock logic
        return {"status": "success", "ai_response": "Based on your concerns, you should focus on hydration and sleep."}
