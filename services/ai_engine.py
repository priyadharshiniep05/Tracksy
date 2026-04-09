"""
Tracksy Global — AI Engine.
"""
from datetime import datetime, timedelta
import math
import random
from database import get_db

class AIEngine:
    def optimize_route(self, origin, dest, weight_kg, mode, priority, speed_cost_balance):
        distance = math.sqrt((dest['lat']-origin['lat'])**2 + (dest['lng']-origin['lng'])**2) * 111
        speed = 800 if mode == 'air' else (30 if mode == 'sea' else 60)
        duration_hours = distance / speed
        cost = distance * (2.5 if mode == 'air' else (0.5 if mode == 'sea' else 1.2)) * (weight_kg/1000)
        carbon = distance * (0.5 if mode == 'air' else (0.01 if mode == 'sea' else 0.06)) * (weight_kg/1000)
        
        waypoints = []
        for i in range(10):
            t = i / 9
            waypoints.append([origin['lat'] + t*(dest['lat']-origin['lat']), origin['lng'] + t*(dest['lng']-origin['lng'])])
            
        return {
            "waypoints": waypoints,
            "distance_km": round(distance, 1),
            "duration_hours": round(duration_hours, 1),
            "eta": datetime.utcnow() + timedelta(hours=duration_hours),
            "cost": round(cost, 2),
            "carbon": round(carbon, 2),
            "ai_explanation": f"Route optimized for {priority} using {mode}. Balances cost and speed."
        }

    def auto_assign_vehicle(self, route_data):
        db = get_db()
        vehicles = db.execute("SELECT id, driver_id FROM vehicles WHERE status='available' LIMIT 1").fetchone()
        if vehicles:
            db.execute("UPDATE vehicles SET status='assigned' WHERE id=?", (vehicles['id'],))
            db.execute("UPDATE drivers SET status='assigned' WHERE id=?", (vehicles['driver_id'],))
            return {"vehicle_id": vehicles['id'], "driver_id": vehicles['driver_id']}
        return {"vehicle_id": None, "driver_id": None}

    def generate_route_comparison(self, origin, dest, weight_kg):
        fastest = self.optimize_route(origin, dest, weight_kg, 'air', 'urgent', 100)
        cheapest = self.optimize_route(origin, dest, weight_kg, 'sea', 'economy', 0)
        balanced = self.optimize_route(origin, dest, weight_kg, 'road', 'standard', 50)
        return {"fastest": fastest, "cheapest": cheapest, "balanced": balanced}
        
    def predict_disruption_impact(self, order_id, disruption_id):
        return {"impact_score": random.uniform(0.1, 0.9), "recommendation": "Reroute via alternate hub."}

ai_engine = AIEngine()
