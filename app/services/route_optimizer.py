import math
from typing import List, Dict, Any
from app.models import TransportMode, Priority
from app.config import settings

class RouteOptimizer:
    """
    Multi-objective route optimizer with multimodal support.
    """
    
    # Cost model per km per kg
    COST_MODEL = {
        TransportMode.ROAD: {"per_km_kg": 0.0012, "fixed_km": 0.0008, "speed": 65},
        TransportMode.AIR: {"per_km_kg": 0.008, "fixed_km": 0.003, "speed": 850},
        TransportMode.SEA: {"per_km_kg": 0.0003, "fixed_km": 0.00015, "speed": 22},
        TransportMode.RAIL: {"per_km_kg": 0.0006, "fixed_km": 0.0003, "speed": 120}
    }

    # Carbon model (kg CO2 per tonne-km)
    CARBON_MODEL = {
        TransportMode.ROAD: 0.096,
        TransportMode.AIR: 0.602,
        TransportMode.SEA: 0.019,
        TransportMode.RAIL: 0.028
    }

    async def optimize(
        self, 
        origin: Dict[str, float], 
        dest: Dict[str, float], 
        weight_kg: float, 
        priority: Priority, 
        mode_pref: TransportMode = TransportMode.ROAD,
        slider: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Computes top 3 routes based on cost, speed, and carbon.
        """
        distance = self._haversine(origin['lat'], origin['lon'], dest['lat'], dest['lon'])
        
        routes = []
        for mode in [TransportMode.ROAD, TransportMode.AIR, TransportMode.SEA, TransportMode.RAIL]:
            route_data = self._calculate_route_metrics(mode, distance, weight_kg, slider)
            routes.append(route_data)
            
        # Add multimodal option if distance is large
        if distance > 1000:
            routes.append(self._calculate_multimodal_route(origin, dest, distance, weight_kg, slider))
            
        # Sort by combined score
        routes.sort(key=lambda x: x['combined_score'])
        return routes[:3]

    def _calculate_route_metrics(self, mode: TransportMode, distance: float, weight_kg: float, slider: float) -> Dict[str, Any]:
        cfg = self.COST_MODEL.get(mode, self.COST_MODEL[TransportMode.ROAD])
        
        time_hours = distance / cfg['speed']
        cost = (cfg['per_km_kg'] * distance * weight_kg) + (cfg['fixed_km'] * distance)
        carbon = (self.CARBON_MODEL.get(mode, 0.096) * (weight_kg / 1000) * distance)
        
        # Normalized scores (simplified for demo)
        time_score = min(time_hours / 500, 1.0)
        cost_score = min(cost / 5000, 1.0)
        carbon_score = min(carbon / 1000, 1.0)
        
        combined_score = (slider * time_score) + ((1 - slider) * cost_score) + (0.15 * carbon_score)
        
        return {
            "mode": mode,
            "distance_km": round(distance, 2),
            "estimated_hours": round(time_hours, 1),
            "cost_usd": round(cost, 2),
            "carbon_kg": round(carbon, 2),
            "combined_score": combined_score,
            "explanation": f"Strategic {mode.value} route covering {round(distance)}km."
        }

    def _calculate_multimodal_route(self, origin, dest, distance, weight_kg, slider) -> Dict[str, Any]:
        # Simple multimodal simulation: road (10%) + air/sea (80%) + road (10%)
        mode = TransportMode.MULTIMODAL
        time_hours = (distance * 0.2 / 65) + (distance * 0.8 / 400) # Blended speed
        cost = (0.004 * distance * weight_kg) + (0.002 * distance)
        carbon = (0.3 * (weight_kg / 1000) * distance)
        
        time_score = min(time_hours / 500, 1.0)
        cost_score = min(cost / 5000, 1.0)
        carbon_score = min(carbon / 1000, 1.0)
        
        combined_score = (slider * time_score) + ((1 - slider) * cost_score) + (0.15 * carbon_score)
        
        return {
            "mode": mode,
            "distance_km": round(distance, 2),
            "estimated_hours": round(time_hours, 1),
            "cost_usd": round(cost, 2),
            "carbon_kg": round(carbon, 2),
            "combined_score": combined_score,
            "explanation": "Optimized multimodal route balancing speed and cost."
        }

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

route_optimizer = RouteOptimizer()
