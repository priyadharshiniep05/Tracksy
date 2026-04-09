from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

class ETARegressor:
    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=100)
        self.is_trained = False

    def train_synthetic(self):
        X = np.random.rand(500, 5) * 100
        y = np.random.rand(500) * 48  # target = hours
        self.model.fit(X, y)
        self.is_trained = True

    def predict_eta_hours(self, features_dict):
        if not self.is_trained: self.train_synthetic()
        f = [features_dict.get('distance_km', 100), features_dict.get('weight_kg', 1000), 1, 0.5, 0]
        pred = self.model.predict([f])[0]
        return float(pred)
