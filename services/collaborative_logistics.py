"""
Tracksy Global — Collaborative Logistics.
"""
from database import get_db

class CollaborativeLogistics:
    def find_spare_capacity(self, corridor):
        db = get_db()
        slots = db.execute("SELECT * FROM collaborative_slots WHERE route_corridor LIKE ? AND status='available'", (f"%{corridor}%",)).fetchall()
        return [dict(s) for s in slots]

collaborative_logistics = CollaborativeLogistics()
