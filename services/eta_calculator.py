"""
Tracksy Global — ETA Calculator.
"""
from ml.eta_regressor import eta_regressor
from datetime import datetime, timedelta

class ETACalculator:
    def calculate_eta(self, order_data):
        hours = eta_regressor.predict_eta_hours(order_data)
        eta = datetime.utcnow() + timedelta(hours=hours)
        return eta

eta_calculator = ETACalculator()
