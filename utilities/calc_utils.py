def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI given weight in kg and height in cm.
    """
    try:
        height_m = float(height_cm) / 100
        weight = float(weight_kg)
        if height_m <= 0 or weight <= 0:
            return None, "Invalid height or weight"
        
        bmi = weight / (height_m * height_m)
        
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
            
        return {"bmi": round(bmi, 2), "category": category}, None
    except Exception as e:
        return None, str(e)
