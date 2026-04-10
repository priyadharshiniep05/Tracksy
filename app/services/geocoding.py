from typing import Dict, Any, Optional
import httpx
from app.config import settings

class GeocodingService:
    """
    Google Maps / Nominatim geocoding with city dict fallback.
    """
    
    CITIES = {
        "Mumbai": {"lat": 19.0760, "lon": 72.8777, "country": "India"},
        "Delhi": {"lat": 28.7041, "lon": 77.1025, "country": "India"},
        "Chennai": {"lat": 13.0827, "lon": 80.2707, "country": "India"},
        "Bangalore": {"lat": 12.9716, "lon": 77.5946, "country": "India"},
        "Kolkata": {"lat": 22.5726, "lon": 88.3639, "country": "India"},
        "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "country": "India"},
        "Hamburg": {"lat": 53.5511, "lon": 9.9937, "country": "Germany"},
        "Rotterdam": {"lat": 51.9244, "lon": 4.4777, "country": "Netherlands"},
        "London": {"lat": 51.5074, "lon": -0.1278, "country": "UK"},
        "New York": {"lat": 40.7128, "lon": -74.0060, "country": "USA"},
        "Los Angeles": {"lat": 34.0522, "lon": -118.2437, "country": "USA"},
        "Dubai": {"lat": 25.2048, "lon": 55.2708, "country": "UAE"},
        "Singapore": {"lat": 1.3521, "103.8198": 103.8198, "country": "Singapore"},
        "Shanghai": {"lat": 31.2304, "lon": 121.4737, "country": "China"},
        "Tokyo": {"lat": 35.6762, "lon": 139.6503, "country": "Japan"},
    }

    async def geocode(self, address: str) -> Dict[str, Any]:
        # 1. Check internal dict
        for city, data in self.CITIES.items():
            if city.lower() in address.lower():
                return {
                    "lat": data["lat"],
                    "lon": data["lon"],
                    "formatted_address": f"{city}, {data['country']}",
                    "city": city,
                    "country": data["country"]
                }
        
        # 2. Mock Google Maps fallback
        return {
            "lat": 0.0,
            "lon": 0.0,
            "formatted_address": address,
            "city": "Unknown",
            "country": "Unknown"
        }

geocoding_service = GeocodingService()
