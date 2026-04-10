from datetime import datetime, timedelta
from typing import Dict, Any
from app.models import TransportMode
from app.services.weather_service import weather_service
from app.services.traffic_service import traffic_service

class ETAEngine:
    """
    AI-style ETA engine: distance + traffic + weather + historical factors.
    """
    
    SPEEDS = {
        TransportMode.ROAD: 65,
        TransportMode.AIR: 850,
        TransportMode.SEA: 22,
        TransportMode.RAIL: 120,
        TransportMode.MULTIMODAL: 150
    }

    async def calculate_eta(
        self, 
        mode: TransportMode, 
        distance_km: float, 
        lat: float, 
        lon: float
    ) -> Dict[str, Any]:
        base_speed = self.SPEEDS.get(mode, 65)
        base_hours = distance_km / base_speed
        
        # Traffic Factor
        traffic = await traffic_service.get_traffic(lat, lon)
        traffic_factor = traffic['flow_ratio'] # 1.0 is normal, higher is slower
        
        # Weather Factor
        weather = await weather_service.get_weather(lat, lon)
        weather_factor = weather['delay_factor'] # 1.0 is clear
        
        # Historical factor (simulated for now, would come from ml_model.py)
        historical_factor = 1.05 
        
        final_hours = base_hours * traffic_factor * weather_factor * historical_factor
        eta_datetime = datetime.utcnow() + timedelta(hours=final_hours)
        
        confidence = 0.85 if mode == TransportMode.ROAD else 0.92
        delay_prob = (traffic_factor - 1.0) * 100 + (weather_factor - 1.0) * 50
        
        return {
            "eta": eta_datetime,
            "confidence_pct": round(confidence * 100, 1),
            "delay_probability_pct": round(max(0, min(100, delay_prob)), 1),
            "breakdown": {
                "base_hours": round(base_hours, 1),
                "traffic_impact": f"{round((traffic_factor-1)*100)}%",
                "weather_impact": f"{round((weather_factor-1)*100)}%",
                "condition": weather['condition']
            }
        }

eta_engine = ETAEngine()
