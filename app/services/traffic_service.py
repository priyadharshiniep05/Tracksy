import datetime
import random
from typing import Dict, Any
from app.config import settings

class TrafficService:
    """
    TomTom Traffic Flow API with fallback simulation.
    """
    
    async def get_traffic(self, lat: float, lon: float) -> Dict[str, Any]:
        if settings.TOMTOM_API_KEY:
            try:
                # Actual API call would go here
                pass
            except Exception:
                pass
        
        return self._simulate_traffic()

    def _simulate_traffic(self) -> Dict[str, Any]:
        hour = datetime.datetime.now().hour
        
        # Rush hour simulation
        if (8 <= hour <= 10) or (17 <= hour <= 19):
            flow = 1.3 + (random.random() * 0.3) # 1.3x to 1.6x delay
            level = "Heavy"
        elif 0 <= hour <= 5:
            flow = 0.85
            level = "Low"
        else:
            flow = 1.0
            level = "Moderate"
            
        return {
            "flow_ratio": flow,
            "delay_minutes": round((flow - 1.0) * 30),
            "congestion_level": level
        }

traffic_service = TrafficService()
