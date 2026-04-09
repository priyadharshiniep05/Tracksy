import random
from services.ai_engine import reroute_order
from database import get_db

def trigger_random_disruption(socketio=None):
    db = get_db()
    with db:
        in_transit = db.execute("SELECT id FROM orders WHERE status='in_transit'").fetchall()
        if not in_transit:
            return None
        
        target = random.choice(in_transit)['id']
        disruption_types = ['accident', 'weather', 'road_closure', 'vehicle_breakdown']
        dtype = random.choice(disruption_types)
        
        db.execute("INSERT INTO disruption_log (order_id, type, description, detected_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                   (target, dtype, f"Simulated {dtype} disruption"))
        
        reroute_order(target, dtype, socketio)
        return target, dtype
