import pickle
import os
import sys
import __main__

# Ensure the models path is in sys.path and import MockModel so unpickling works
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.mock_model import MockModel

# Inject into __main__ because it was pickled as __main__.MockModel
__main__.MockModel = MockModel

class PredictionService:
    def __init__(self):
        self.model = self._load_model()

    def _load_model(self):
        """
        Loads the mock ML model from disk.
        """
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'deficiency_model.pkl')
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except FileNotFoundError:
            return None

    def predict(self, symptoms):
        """
        Processes symptoms and returns a prediction.
        """
        if not self.model:
            raise Exception("Prediction model not found. Please train/create the model first.")

        # In a real scenario, we would use utility functions to preprocess the input
        # formatted_data = preprocess_data(symptoms)

        try:
            prediction = self.model.predict([symptoms])
            risk = prediction[0] if isinstance(prediction, (list, tuple)) else prediction
            return {"deficiency_risk": risk}
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
