"""
Tracksy Global — Multimodal Router.
"""
import math

class MultimodalRouter:
    def find_nearest_hub(self, coords, hub_type):
        # Dummy implementation
        return {"name": f"Nearest {hub_type.capitalize()}", "lat": coords['lat'] + 0.1, "lng": coords['lng'] + 0.1}

    def build_route(self, origin, dest, mode, weight, priority):
        dist = math.sqrt((dest['lat']-origin['lat'])**2 + (dest['lng']-origin['lng'])**2) * 111
        if mode in ['air', 'sea', 'multimodal']:
            hub1 = self.find_nearest_hub(origin, 'airport' if mode == 'air' else 'port')
            hub2 = self.find_nearest_hub(dest, 'airport' if mode == 'air' else 'port')
            return [
                {"mode": "road", "start": origin, "end": hub1, "distance": 50},
                {"mode": mode, "start": hub1, "end": hub2, "distance": dist},
                {"mode": "road", "start": hub2, "end": dest, "distance": 50}
            ]
        else:
            return [{"mode": "road", "start": origin, "end": dest, "distance": dist}]

    def calculate_leg_metrics(self, leg):
        dist = leg['distance']
        mode = leg['mode']
        cost = dist * (2.5 if mode == 'air' else (0.5 if mode == 'sea' else 1.2))
        carbon = dist * (0.5 if mode == 'air' else (0.01 if mode == 'sea' else 0.06))
        duration = dist / (800 if mode == 'air' else (30 if mode == 'sea' else 60))
        return {"cost": cost, "carbon": carbon, "duration_hours": duration}

multimodal_router = MultimodalRouter()
