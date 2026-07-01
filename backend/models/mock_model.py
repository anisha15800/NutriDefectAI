import pickle
import os

class MockModel:
    """
    A simple mock model to simulate the behavior of a real ML model.
    """
    def __init__(self):
        self.name = "NutriDefect_Mock_Model"

    def predict(self, input_data):
        """
        Simulate a prediction based on some dummy logic.
        """
        results = []
        for item in input_data:
            # Dummy logic: if 'fatigue' is in symptoms, predict Iron deficiency
            symptoms_str = str(item).lower()
            if 'fatigue' in symptoms_str:
                results.append("High Risk: Iron Deficiency")
            elif 'bones' in symptoms_str or 'muscle' in symptoms_str:
                results.append("Moderate Risk: Vitamin D Deficiency")
            else:
                results.append("Low Risk: No major deficiencies detected")
        return results

if __name__ == '__main__':
    model = MockModel()
    model_path = os.path.join(os.path.dirname(__file__), 'deficiency_model.pkl')
    
    print(f"Saving mock model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print("Model saved successfully.")
