"""
Tracksy Global — Carbon Calculator.
"""
class CarbonCalculator:
    def calculate(self, distance_km, weight_kg, mode):
        emission_factors = {'road': 0.062, 'air': 0.500, 'sea': 0.008, 'rail': 0.022}
        factor = emission_factors.get(mode, 0.062)
        base_carbon = distance_km * factor * (weight_kg / 1000)
        
        suggestions = []
        if mode == 'air':
            suggestions.append("Switch to Sea Freight to save 90% CO2")
        if mode == 'road' and distance_km > 1000:
            suggestions.append("Consider Rail for long-haul land transport")
            
        return {
            "carbon_kg": round(base_carbon, 2),
            "offset_cost_usd": round(base_carbon * 0.02, 2), # $20 per ton
            "eco_suggestions": suggestions
        }

carbon_calculator = CarbonCalculator()
