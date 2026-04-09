"""
Tracksy Global — Self Learning Model Feedback.
"""
from database import get_db

class SelfLearning:
    def generate_insight(self):
        db = get_db()
        delayed_orders = db.execute("SELECT COUNT(*) FROM orders WHERE status='delayed'").fetchone()[0]
        if delayed_orders > 5:
            return "Current delay rates are above normal. Suggest retraining ETA regressor."
        return "Model performance is within acceptable bounds."

self_learning = SelfLearning()
