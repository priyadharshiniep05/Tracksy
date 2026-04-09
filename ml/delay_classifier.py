from sklearn.ensemble import RandomForestClassifier
import numpy as np

class DelayClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train_synthetic(self):
        # Features: distance_km, weight_kg, mode(0-4), priority(0-2), weather_risk
        # Generate 500 samples
        X = np.random.rand(500, 5) * 100
        y = np.random.randint(2, size=500)
        self.model.fit(X, y)
        self.is_trained = True

    def predict_delay_probability(self, features_dict):
        if not self.is_trained: self.train_synthetic()
        # Mock specific logic
        # return float 0-1
        f = [features_dict.get('distance_km', 100), features_dict.get('weight_kg', 1000), 1, 1, 0.5]
        probs = self.model.predict_proba([f])[0]
        return float(probs[1])
