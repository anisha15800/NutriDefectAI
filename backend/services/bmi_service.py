import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utilities.calc_utils import calculate_bmi

class BMIService:
    @staticmethod
    def process_bmi(weight, height):
        # Using the utility function
        return calculate_bmi(weight, height)
