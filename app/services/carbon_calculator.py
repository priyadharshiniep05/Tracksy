from app.models import TransportMode

class CarbonCalculator:
    """
    CO2 calculator per mode per km.
    """
    # kg CO2 per tonne-km
    FACTORS = {
        TransportMode.ROAD: 0.096,
        TransportMode.AIR: 0.602,
        TransportMode.SEA: 0.019,
        TransportMode.RAIL: 0.028,
        TransportMode.MULTIMODAL: 0.231 # Weighted average for demo
    }

    def calculate(self, mode: TransportMode, distance_km: float, weight_kg: float) -> float:
        factor = self.FACTORS.get(mode, 0.096)
        tonnes = weight_kg / 1000
        return round(factor * tonnes * distance_km, 2)

carbon_calculator = CarbonCalculator()
