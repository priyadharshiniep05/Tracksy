import os
import joblib

class ModelStore:
    def __init__(self):
        self.save_dir = 'ml/saved_models/'
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_model(self, model, name):
        path = os.path.join(self.save_dir, f"{name}.joblib")
        joblib.dump(model, path)
        return path

    def load_model(self, name):
        path = os.path.join(self.save_dir, f"{name}.joblib")
        if os.path.exists(path):
            return joblib.load(path)
        return None
