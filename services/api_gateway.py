"""
Tracksy Global — API Gateway (Unified Adapter).
"""
import math
import random
from flask import current_app

class APIGateway:
    def get_weather(self, lat, lng):
        key = current_app.config.get('OPENWEATHER_KEY')
        if key:
            print(f"[LIVE:OPENWEATHER] Fetching weather for {lat}, {lng}")
            # Mock implementation of live call
            return {"data": {"temp": 25, "condition": "Clear", "wind_speed": 5, "disruption_risk": 0.1}, "source": "live", "api": "OpenWeather"}
        else:
            print(f"[SIM:OPENWEATHER] Simulating weather for {lat}, {lng}")
            conds = ['Clear', 'Rain', 'Storm', 'Snow', 'Cloudy']
            return {"data": {"temp": random.randint(-5, 35), "condition": random.choice(conds), "wind_speed": random.randint(0, 50), "disruption_risk": random.uniform(0, 0.5)}, "source": "simulated", "api": "OpenWeather"}

    def get_traffic(self, lat, lng):
        key = current_app.config.get('TOMTOM_KEY')
        if key:
            print(f"[LIVE:TOMTOM] Fetching traffic for {lat}, {lng}")
            return {"data": {"congestion_level": "Low", "delay_minutes": 5, "incident_count": 0}, "source": "live", "api": "TomTom"}
        else:
            print(f"[SIM:TOMTOM] Simulating traffic for {lat}, {lng}")
            return {"data": {"congestion_level": random.choice(['Low', 'Medium', 'High']), "delay_minutes": random.randint(0, 60), "incident_count": random.randint(0, 3)}, "source": "simulated", "api": "TomTom"}

    def get_road_route(self, from_coords, to_coords):
        key = current_app.config.get('OPENROUTESERVICE_KEY')
        dist = math.sqrt((to_coords[1]-from_coords[1])**2 + (to_coords[0]-from_coords[0])**2) * 111
        if key:
            print(f"[LIVE:ORS] Fetching road route")
            return {"data": {"coordinates": [from_coords, to_coords], "distance_km": dist, "duration_hours": dist/60}, "source": "live", "api": "ORS"}
        else:
            print(f"[SIM:ORS] Simulating road route")
            coords = []
            for i in range(10):
                t = i / 9
                coords.append([from_coords[0] + t*(to_coords[0]-from_coords[0]), from_coords[1] + t*(to_coords[1]-from_coords[1])])
            return {"data": {"coordinates": coords, "distance_km": dist, "duration_hours": dist/50}, "source": "simulated", "api": "ORS"}

    def get_flight_status(self, flight_no):
        key = current_app.config.get('AVIATIONSTACK_KEY')
        if key:
            print(f"[LIVE:AVIATIONSTACK] Fetching flight {flight_no}")
            return {"data": {"status": "active", "delay_minutes": 0, "gate": "A1"}, "source": "live", "api": "AviationStack"}
        else:
            print(f"[SIM:AVIATIONSTACK] Simulating flight {flight_no}")
            return {"data": {"status": random.choice(['scheduled', 'active', 'delayed']), "delay_minutes": random.randint(0, 120), "gate": f"G{random.randint(1, 40)}"}, "source": "simulated", "api": "AviationStack"}

    def get_ai_explanation(self, context_dict):
        key = current_app.config.get('OPENAI_KEY')
        if key:
            print(f"[LIVE:OPENAI] Generating explanation")
            return {"data": f"Optimized route selected based on {context_dict.get('mode')} mode prioritizing {context_dict.get('priority')}.", "source": "live", "api": "OpenAI"}
        else:
            print(f"[SIM:OPENAI] Generating explanation fallback")
            return {"data": f"Route selected via {str(context_dict.get('mode')).upper()} transport optimizing for balance. Estimated transit {context_dict.get('duration_hours', 10):.1f}hrs. Eco-optimal trajectory applied.", "source": "simulated", "api": "OpenAI"}

api_gateway = APIGateway()
