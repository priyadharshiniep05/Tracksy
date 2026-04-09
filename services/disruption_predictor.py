"""
Tracksy Global — Disruption Predictor.
"""
import random
from services.api_gateway import api_gateway
from database import get_db
from datetime import datetime, timedelta

class DisruptionPredictor:
    def __init__(self):
        self.hubs = [
            {"name": "Mumbai", "lat": 19.0760, "lng": 72.8777},
            {"name": "Singapore", "lat": 1.3521, "lng": 103.8198},
            {"name": "Rotterdam", "lat": 51.9244, "lng": 4.4777},
            {"name": "New York", "lat": 40.7128, "lng": -74.0060},
            {"name": "Dubai", "lat": 25.2048, "lng": 55.2708}
        ]

    def run_prediction_cycle(self):
        new_disruptions = []
        for hub in self.hubs:
            weather = api_gateway.get_weather(hub['lat'], hub['lng'])
            if weather['data']['disruption_risk'] > 0.35 and random.random() < 0.2:
                d = {
                    "type": "weather",
                    "severity": "high" if weather['data']['disruption_risk'] > 0.45 else "medium",
                    "region": hub['name'],
                    "lat": hub['lat'],
                    "lng": hub['lng'],
                    "radius": random.randint(50, 200),
                    "title": f"Weather Alert in {hub['name']}",
                    "description": f"High risk of disruption due to {weather['data']['condition']}."
                }
                
                db = get_db()
                db.execute(
                    "INSERT INTO disruptions (type, severity, affected_region, affected_lat, affected_lng, affected_radius_km, title, description, active) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (d['type'], d['severity'], d['region'], d['lat'], d['lng'], d['radius'], d['title'], d['description'])
                )
                db.commit()
                new_disruptions.append(d)
        return new_disruptions
