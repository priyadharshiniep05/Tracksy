"""
Tracksy Global — Digital Twin.
"""
import random

class DigitalTwin:
    def run_monte_carlo(self, order_data, iterations=100):
        etas = []
        costs = []
        for _ in range(iterations):
            delay = random.uniform(0, 48)
            cost_overrun = random.uniform(0, 500)
            etas.append(delay)
            costs.append(cost_overrun)
            
        etas.sort()
        costs.sort()
        return {
            "p50_delay_hours": round(etas[int(iterations*0.5)], 1),
            "p95_delay_hours": round(etas[int(iterations*0.95)], 1),
            "p50_cost_overrun": round(costs[int(iterations*0.5)], 2),
            "risk_events_detected": random.randint(0, 3)
        }

digital_twin = DigitalTwin()
