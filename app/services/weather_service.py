import datetime
from typing import Dict, Any
import httpx
from app.config import settings

class WeatherService:
    """
    OpenWeather API with fallback simulation.
    """
    
    async def get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        if settings.OPENWEATHER_API_KEY:
            try:
                # Actual API call would go here
                pass
            except Exception:
                pass
        
        return self._simulate_weather(lat, lon)

    def _simulate_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        month = datetime.datetime.now().month
        
        # Tropical monsoon simulation
        if abs(lat) < 23.5 and month in [6, 7, 8, 9]:
            return {"condition": "Heavy Rain", "temp_c": 28, "delay_factor": 1.3}
        
        # High latitude winter
        if abs(lat) > 55 and month in [11, 12, 1, 2]:
            return {"condition": "Snow/Storm", "temp_c": -5, "delay_factor": 1.8}
            
        return {"condition": "Clear", "temp_c": 22, "delay_factor": 1.0}

weather_service = WeatherService()
