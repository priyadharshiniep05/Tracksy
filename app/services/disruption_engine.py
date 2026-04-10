import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import DisruptionEvent, Order, Alert, AlertType, AlertSeverity, OrderStatus

class DisruptionEngine:
    """
    Manages DisruptionEvent lifecycle and impacts.
    """
    
    TYPES = [
        {"type": "WEATHER", "desc": "Cyclone warning in Bay of Bengal"},
        {"type": "PORT_CONGESTION", "desc": "Port of Mumbai congestion — 18hr delay"},
        {"type": "STRIKE", "desc": "Customs strike at Delhi Airport"},
        {"type": "TRAFFIC", "desc": "National Highway 48 accident — 4hr blockage"},
        {"type": "STORM", "desc": "Severe thunderstorm — Frankfurt Airport closed 6hrs"}
    ]

    async def simulate_disruption(self) -> Dict[str, Any]:
        async with AsyncSessionLocal() as db:
            template = random.choice(self.TYPES)
            
            disruption = DisruptionEvent(
                type=template['type'],
                severity=random.uniform(0.5, 1.0),
                affected_region=random.choice(["Mumbai", "Delhi", "Chennai", "Europe", "Global"]),
                description=template['desc'],
                ends_at=datetime.utcnow() + timedelta(hours=random.randint(4, 24))
            )
            db.add(disruption)
            
            # Find impacted orders (simplified: check origin/dest city)
            result = await db.execute(
                select(Order).where(
                    (Order.status == OrderStatus.IN_TRANSIT) | (Order.status == OrderStatus.ASSIGNED)
                )
            )
            orders = result.scalars().all()
            impacted = [o for o in orders if disruption.affected_region in [o.origin_city, o.dest_city]]
            
            disruption.impacted_orders_count = len(impacted)
            
            for order in impacted:
                alert = Alert(
                    order_id=order.id,
                    type=AlertType.DISRUPTION,
                    message=f"Order impacted by {disruption.type}: {disruption.description}",
                    severity=AlertSeverity.HIGH
                )
                db.add(alert)
                order.status = OrderStatus.DELAYED
                order.delay_reason = disruption.type
            
            await db.commit()
            return {
                "id": disruption.id,
                "type": disruption.type,
                "description": disruption.description,
                "impacted_count": len(impacted)
            }

disruption_engine = DisruptionEngine()
